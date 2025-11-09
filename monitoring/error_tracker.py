#!/usr/bin/env python3
"""
錯誤追蹤系統
收集、分析和報告系統錯誤
"""

import logging
import json
import sqlite3
import traceback
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from flask import Flask, request, jsonify
import os

# 設定日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ErrorTracker:
    """錯誤追蹤器"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.db_path = config.get('db_path', 'error_tracker.db')
        self.init_database()
        self.setup_logging()
    
    def init_database(self):
        """初始化錯誤追蹤資料庫"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 建立錯誤記錄表格
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS error_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                error_type TEXT NOT NULL,
                error_message TEXT NOT NULL,
                stack_trace TEXT,
                user_id TEXT,
                session_id TEXT,
                request_url TEXT,
                request_method TEXT,
                request_headers TEXT,
                request_body TEXT,
                severity TEXT DEFAULT 'error',
                resolved BOOLEAN DEFAULT FALSE,
                tags TEXT
            )
        ''')
        
        # 建立錯誤統計表格
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS error_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE NOT NULL,
                error_type TEXT NOT NULL,
                count INTEGER DEFAULT 1,
                severity TEXT DEFAULT 'error',
                UNIQUE(date, error_type, severity)
            )
        ''')
        
        # 建立效能錯誤表格
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS performance_errors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                endpoint TEXT NOT NULL,
                response_time REAL NOT NULL,
                status_code INTEGER NOT NULL,
                error_type TEXT,
                error_message TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def setup_logging(self):
        """設定日誌記錄"""
        # 建立錯誤日誌檔案
        error_logger = logging.getLogger('error_tracker')
        error_handler = logging.FileHandler('error_tracker.log')
        error_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        error_handler.setFormatter(error_formatter)
        error_logger.addHandler(error_handler)
        error_logger.setLevel(logging.ERROR)
    
    def log_error(self, 
                  error_type: str,
                  error_message: str,
                  stack_trace: str = None,
                  user_id: str = None,
                  session_id: str = None,
                  request_data: Dict = None,
                  severity: str = 'error',
                  tags: List[str] = None):
        """記錄錯誤"""
        
        # 準備請求資料
        request_url = None
        request_method = None
        request_headers = None
        request_body = None
        
        if request_data:
            request_url = request_data.get('url')
            request_method = request_data.get('method')
            request_headers = json.dumps(request_data.get('headers', {}))
            request_body = request_data.get('body')
        
        # 儲存到資料庫
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO error_logs 
            (error_type, error_message, stack_trace, user_id, session_id,
             request_url, request_method, request_headers, request_body,
             severity, tags)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            error_type,
            error_message,
            stack_trace,
            user_id,
            session_id,
            request_url,
            request_method,
            request_headers,
            request_body,
            severity,
            json.dumps(tags) if tags else None
        ))
        
        conn.commit()
        conn.close()
        
        # 更新錯誤統計
        self.update_error_stats(error_type, severity)
        
        # 記錄到日誌檔案
        error_logger = logging.getLogger('error_tracker')
        error_logger.error(f"{error_type}: {error_message}")
        
        logger.info(f"錯誤已記錄: {error_type} - {error_message}")
    
    def log_api_error(self, endpoint: str, status_code: int, 
                     response_time: float, error_message: str = None):
        """記錄 API 錯誤"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO performance_errors 
            (endpoint, response_time, status_code, error_message)
            VALUES (?, ?, ?, ?)
        ''', (endpoint, response_time, status_code, error_message))
        
        conn.commit()
        conn.close()
    
    def update_error_stats(self, error_type: str, severity: str):
        """更新錯誤統計"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        today = datetime.now().date()
        
        cursor.execute('''
            INSERT OR REPLACE INTO error_stats (date, error_type, count, severity)
            VALUES (?, ?, 
                COALESCE((SELECT count FROM error_stats 
                         WHERE date = ? AND error_type = ? AND severity = ?), 0) + 1,
                ?)
        ''', (today, today, error_type, severity, severity))
        
        conn.commit()
        conn.close()
    
    def get_error_summary(self, days: int = 7) -> Dict:
        """取得錯誤摘要"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        start_date = datetime.now() - timedelta(days=days)
        
        # 錯誤總數
        cursor.execute('''
            SELECT COUNT(*) FROM error_logs 
            WHERE timestamp >= ?
        ''', (start_date,))
        total_errors = cursor.fetchone()[0]
        
        # 按類型分組
        cursor.execute('''
            SELECT error_type, COUNT(*) as count
            FROM error_logs 
            WHERE timestamp >= ?
            GROUP BY error_type
            ORDER BY count DESC
        ''', (start_date,))
        errors_by_type = dict(cursor.fetchall())
        
        # 按嚴重程度分組
        cursor.execute('''
            SELECT severity, COUNT(*) as count
            FROM error_logs 
            WHERE timestamp >= ?
            GROUP BY severity
        ''', (start_date,))
        errors_by_severity = dict(cursor.fetchall())
        
        # 最近錯誤
        cursor.execute('''
            SELECT error_type, error_message, timestamp, severity
            FROM error_logs 
            WHERE timestamp >= ?
            ORDER BY timestamp DESC
            LIMIT 10
        ''', (start_date,))
        recent_errors = cursor.fetchall()
        
        # API 錯誤統計
        cursor.execute('''
            SELECT endpoint, COUNT(*) as count, AVG(response_time) as avg_time
            FROM performance_errors 
            WHERE timestamp >= ?
            GROUP BY endpoint
            ORDER BY count DESC
        ''', (start_date,))
        api_errors = cursor.fetchall()
        
        conn.close()
        
        return {
            'summary': {
                'total_errors': total_errors,
                'period_days': days,
                'errors_by_type': errors_by_type,
                'errors_by_severity': errors_by_severity
            },
            'recent_errors': [
                {
                    'type': error[0],
                    'message': error[1],
                    'timestamp': error[2],
                    'severity': error[3]
                }
                for error in recent_errors
            ],
            'api_errors': [
                {
                    'endpoint': error[0],
                    'count': error[1],
                    'avg_response_time': error[2]
                }
                for error in api_errors
            ]
        }
    
    def get_error_trends(self, days: int = 30) -> Dict:
        """取得錯誤趨勢"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        start_date = datetime.now() - timedelta(days=days)
        
        # 每日錯誤統計
        cursor.execute('''
            SELECT DATE(timestamp) as date, COUNT(*) as count
            FROM error_logs 
            WHERE timestamp >= ?
            GROUP BY DATE(timestamp)
            ORDER BY date
        ''', (start_date,))
        daily_errors = dict(cursor.fetchall())
        
        # 錯誤類型趨勢
        cursor.execute('''
            SELECT DATE(timestamp) as date, error_type, COUNT(*) as count
            FROM error_logs 
            WHERE timestamp >= ?
            GROUP BY DATE(timestamp), error_type
            ORDER BY date, error_type
        ''', (start_date,))
        type_trends = cursor.fetchall()
        
        conn.close()
        
        # 組織趨勢資料
        trends = {}
        for date, error_type, count in type_trends:
            if date not in trends:
                trends[date] = {}
            trends[date][error_type] = count
        
        return {
            'daily_errors': daily_errors,
            'type_trends': trends
        }
    
    def get_critical_errors(self) -> List[Dict]:
        """取得嚴重錯誤"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT error_type, error_message, timestamp, stack_trace
            FROM error_logs 
            WHERE severity = 'critical' AND resolved = FALSE
            ORDER BY timestamp DESC
            LIMIT 20
        ''')
        
        critical_errors = cursor.fetchall()
        conn.close()
        
        return [
            {
                'type': error[0],
                'message': error[1],
                'timestamp': error[2],
                'stack_trace': error[3]
            }
            for error in critical_errors
        ]
    
    def mark_error_resolved(self, error_id: int):
        """標記錯誤為已解決"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE error_logs 
            SET resolved = TRUE 
            WHERE id = ?
        ''', (error_id,))
        
        conn.commit()
        conn.close()
    
    def cleanup_old_errors(self, days: int = 90):
        """清理舊錯誤記錄"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cutoff_date = datetime.now() - timedelta(days=days)
        
        cursor.execute('''
            DELETE FROM error_logs 
            WHERE timestamp < ? AND resolved = TRUE
        ''', (cutoff_date,))
        
        deleted_count = cursor.rowcount
        conn.commit()
        conn.close()
        
        logger.info(f"清理了 {deleted_count} 條舊錯誤記錄")
        return deleted_count

class ErrorTrackingMiddleware:
    """錯誤追蹤中間件"""
    
    def __init__(self, app: Flask, error_tracker: ErrorTracker):
        self.app = app
        self.error_tracker = error_tracker
        self.setup_error_handlers()
    
    def setup_error_handlers(self):
        """設定錯誤處理器"""
        
        @self.app.errorhandler(404)
        def handle_404(error):
            self.error_tracker.log_error(
                'not_found',
                str(error),
                request_data={
                    'url': request.url,
                    'method': request.method,
                    'headers': dict(request.headers),
                    'body': request.get_data(as_text=True)
                },
                severity='warning'
            )
            return jsonify({'error': 'Not Found'}), 404
        
        @self.app.errorhandler(500)
        def handle_500(error):
            self.error_tracker.log_error(
                'internal_server_error',
                str(error),
                stack_trace=traceback.format_exc(),
                request_data={
                    'url': request.url,
                    'method': request.method,
                    'headers': dict(request.headers),
                    'body': request.get_data(as_text=True)
                },
                severity='critical'
            )
            return jsonify({'error': 'Internal Server Error'}), 500
        
        @self.app.errorhandler(Exception)
        def handle_exception(error):
            self.error_tracker.log_error(
                'unhandled_exception',
                str(error),
                stack_trace=traceback.format_exc(),
                request_data={
                    'url': request.url,
                    'method': request.method,
                    'headers': dict(request.headers),
                    'body': request.get_data(as_text=True)
                },
                severity='critical'
            )
            return jsonify({'error': 'An unexpected error occurred'}), 500

def main():
    """主函數 - 錯誤追蹤報告"""
    config = {
        'db_path': os.getenv('ERROR_TRACKER_DB', 'error_tracker.db')
    }
    
    tracker = ErrorTracker(config)
    
    # 生成錯誤報告
    print("\n" + "="*60)
    print("🚨 錯誤追蹤報告")
    print("="*60)
    
    # 錯誤摘要
    summary = tracker.get_error_summary(7)
    print(f"\n📊 過去 7 天錯誤摘要:")
    print(f"  總錯誤數: {summary['summary']['total_errors']}")
    print(f"  按類型分佈: {summary['summary']['errors_by_type']}")
    print(f"  按嚴重程度分佈: {summary['summary']['errors_by_severity']}")
    
    # 最近錯誤
    if summary['recent_errors']:
        print(f"\n🕐 最近錯誤 (前 5 個):")
        for error in summary['recent_errors'][:5]:
            print(f"  [{error['severity'].upper()}] {error['type']}: {error['message']}")
    
    # API 錯誤
    if summary['api_errors']:
        print(f"\n🌐 API 錯誤統計:")
        for api_error in summary['api_errors']:
            print(f"  {api_error['endpoint']}: {api_error['count']} 次錯誤, 平均回應時間 {api_error['avg_response_time']:.2f}ms")
    
    # 嚴重錯誤
    critical_errors = tracker.get_critical_errors()
    if critical_errors:
        print(f"\n🚨 嚴重錯誤 (未解決):")
        for error in critical_errors[:3]:
            print(f"  {error['type']}: {error['message']}")
    else:
        print(f"\n✅ 無嚴重錯誤")
    
    # 錯誤趨勢
    trends = tracker.get_error_trends(7)
    if trends['daily_errors']:
        print(f"\n📈 每日錯誤趨勢 (過去 7 天):")
        for date, count in list(trends['daily_errors'].items())[-7:]:
            print(f"  {date}: {count} 個錯誤")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    main()
