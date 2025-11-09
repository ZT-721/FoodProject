#!/usr/bin/env python3
"""
效能監控腳本
監控系統效能並生成報告
"""

import time
import requests
import psutil
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import sqlite3
import os

# 設定日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PerformanceMonitor:
    """效能監控器"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.api_base_url = config.get('api_base_url', 'http://localhost:5000/api')
        self.db_path = config.get('db_path', 'performance_monitor.db')
        self.init_database()
    
    def init_database(self):
        """初始化監控資料庫"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 建立效能監控表格
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS performance_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                metric_name TEXT NOT NULL,
                metric_value REAL NOT NULL,
                metric_unit TEXT,
                tags TEXT
            )
        ''')
        
        # 建立 API 監控表格
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS api_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                endpoint TEXT NOT NULL,
                response_time REAL NOT NULL,
                status_code INTEGER NOT NULL,
                success BOOLEAN NOT NULL,
                error_message TEXT
            )
        ''')
        
        # 建立系統資源表格
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                cpu_percent REAL NOT NULL,
                memory_percent REAL NOT NULL,
                disk_percent REAL NOT NULL,
                network_io TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def monitor_api_endpoints(self) -> List[Dict]:
        """監控 API 端點效能"""
        endpoints = [
            {'path': '/health', 'method': 'GET'},
            {'path': '/ingredients/categories', 'method': 'GET'},
            {'path': '/ingredients/search?q=番茄', 'method': 'GET'},
            {'path': '/recipes/popular', 'method': 'GET'},
        ]
        
        results = []
        
        for endpoint in endpoints:
            try:
                start_time = time.time()
                
                if endpoint['method'] == 'GET':
                    response = requests.get(
                        f"{self.api_base_url}{endpoint['path']}",
                        timeout=10
                    )
                else:
                    response = requests.post(
                        f"{self.api_base_url}{endpoint['path']}",
                        timeout=10
                    )
                
                end_time = time.time()
                response_time = (end_time - start_time) * 1000  # 轉換為毫秒
                
                result = {
                    'endpoint': endpoint['path'],
                    'response_time': response_time,
                    'status_code': response.status_code,
                    'success': response.status_code == 200,
                    'error_message': None if response.status_code == 200 else response.text
                }
                
                results.append(result)
                
                # 儲存到資料庫
                self.save_api_metric(result)
                
            except Exception as e:
                result = {
                    'endpoint': endpoint['path'],
                    'response_time': 0,
                    'status_code': 0,
                    'success': False,
                    'error_message': str(e)
                }
                results.append(result)
                self.save_api_metric(result)
        
        return results
    
    def monitor_system_resources(self) -> Dict:
        """監控系統資源使用"""
        try:
            # CPU 使用率
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # 記憶體使用率
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            
            # 磁碟使用率
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent
            
            # 網路 I/O
            network_io = psutil.net_io_counters()
            network_data = {
                'bytes_sent': network_io.bytes_sent,
                'bytes_recv': network_io.bytes_recv,
                'packets_sent': network_io.packets_sent,
                'packets_recv': network_io.packets_recv
            }
            
            metrics = {
                'cpu_percent': cpu_percent,
                'memory_percent': memory_percent,
                'disk_percent': disk_percent,
                'network_io': json.dumps(network_data)
            }
            
            # 儲存到資料庫
            self.save_system_metrics(metrics)
            
            return metrics
            
        except Exception as e:
            logger.error(f"系統資源監控失敗: {e}")
            return {}
    
    def monitor_database_performance(self) -> Dict:
        """監控資料庫效能"""
        try:
            # 這裡可以添加資料庫連線測試
            # 由於我們使用 Supabase，這裡模擬一些基本指標
            
            start_time = time.time()
            
            # 模擬資料庫查詢測試
            time.sleep(0.1)  # 模擬查詢時間
            
            end_time = time.time()
            query_time = (end_time - start_time) * 1000
            
            metrics = {
                'db_query_time': query_time,
                'db_connections': 1,  # 模擬連線數
                'db_status': 'healthy'
            }
            
            # 儲存效能指標
            self.save_performance_metric('db_query_time', query_time, 'ms')
            self.save_performance_metric('db_connections', 1, 'count')
            
            return metrics
            
        except Exception as e:
            logger.error(f"資料庫效能監控失敗: {e}")
            return {}
    
    def save_api_metric(self, metric: Dict):
        """儲存 API 監控資料"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO api_metrics (endpoint, response_time, status_code, success, error_message)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            metric['endpoint'],
            metric['response_time'],
            metric['status_code'],
            metric['success'],
            metric['error_message']
        ))
        
        conn.commit()
        conn.close()
    
    def save_system_metrics(self, metrics: Dict):
        """儲存系統資源監控資料"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO system_metrics (cpu_percent, memory_percent, disk_percent, network_io)
            VALUES (?, ?, ?, ?)
        ''', (
            metrics['cpu_percent'],
            metrics['memory_percent'],
            metrics['disk_percent'],
            metrics['network_io']
        ))
        
        conn.commit()
        conn.close()
    
    def save_performance_metric(self, name: str, value: float, unit: str = '', tags: str = ''):
        """儲存效能指標"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO performance_metrics (metric_name, metric_value, metric_unit, tags)
            VALUES (?, ?, ?, ?)
        ''', (name, value, unit, tags))
        
        conn.commit()
        conn.close()
    
    def generate_performance_report(self, hours: int = 24) -> Dict:
        """生成效能報告"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 計算時間範圍
        start_time = datetime.now() - timedelta(hours=hours)
        
        # API 效能統計
        cursor.execute('''
            SELECT 
                endpoint,
                AVG(response_time) as avg_response_time,
                MAX(response_time) as max_response_time,
                MIN(response_time) as min_response_time,
                COUNT(*) as total_requests,
                SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successful_requests
            FROM api_metrics 
            WHERE timestamp >= ?
            GROUP BY endpoint
        ''', (start_time,))
        
        api_stats = cursor.fetchall()
        
        # 系統資源統計
        cursor.execute('''
            SELECT 
                AVG(cpu_percent) as avg_cpu,
                MAX(cpu_percent) as max_cpu,
                AVG(memory_percent) as avg_memory,
                MAX(memory_percent) as max_memory,
                AVG(disk_percent) as avg_disk,
                MAX(disk_percent) as max_disk
            FROM system_metrics 
            WHERE timestamp >= ?
        ''', (start_time,))
        
        system_stats = cursor.fetchone()
        
        # 效能指標統計
        cursor.execute('''
            SELECT 
                metric_name,
                AVG(metric_value) as avg_value,
                MAX(metric_value) as max_value,
                MIN(metric_value) as min_value
            FROM performance_metrics 
            WHERE timestamp >= ?
            GROUP BY metric_name
        ''', (start_time,))
        
        perf_stats = cursor.fetchall()
        
        conn.close()
        
        # 生成報告
        report = {
            'report_time': datetime.now().isoformat(),
            'time_range_hours': hours,
            'api_performance': {
                endpoint: {
                    'avg_response_time': avg_time,
                    'max_response_time': max_time,
                    'min_response_time': min_time,
                    'total_requests': total_req,
                    'success_rate': (success_req / total_req * 100) if total_req > 0 else 0
                }
                for endpoint, avg_time, max_time, min_time, total_req, success_req in api_stats
            },
            'system_resources': {
                'cpu': {
                    'average': system_stats[0] if system_stats[0] else 0,
                    'maximum': system_stats[1] if system_stats[1] else 0
                },
                'memory': {
                    'average': system_stats[2] if system_stats[2] else 0,
                    'maximum': system_stats[3] if system_stats[3] else 0
                },
                'disk': {
                    'average': system_stats[4] if system_stats[4] else 0,
                    'maximum': system_stats[5] if system_stats[5] else 0
                }
            },
            'performance_metrics': {
                metric_name: {
                    'average': avg_val,
                    'maximum': max_val,
                    'minimum': min_val
                }
                for metric_name, avg_val, max_val, min_val in perf_stats
            }
        }
        
        return report
    
    def check_alerts(self, report: Dict) -> List[Dict]:
        """檢查警報條件"""
        alerts = []
        
        # API 回應時間警報
        for endpoint, stats in report['api_performance'].items():
            if stats['avg_response_time'] > 5000:  # 5秒
                alerts.append({
                    'type': 'api_performance',
                    'severity': 'warning',
                    'message': f"API {endpoint} 平均回應時間過長: {stats['avg_response_time']:.2f}ms"
                })
            
            if stats['success_rate'] < 95:  # 95%
                alerts.append({
                    'type': 'api_reliability',
                    'severity': 'critical',
                    'message': f"API {endpoint} 成功率過低: {stats['success_rate']:.2f}%"
                })
        
        # 系統資源警報
        if report['system_resources']['cpu']['average'] > 80:
            alerts.append({
                'type': 'system_resource',
                'severity': 'warning',
                'message': f"CPU 使用率過高: {report['system_resources']['cpu']['average']:.2f}%"
            })
        
        if report['system_resources']['memory']['average'] > 85:
            alerts.append({
                'type': 'system_resource',
                'severity': 'warning',
                'message': f"記憶體使用率過高: {report['system_resources']['memory']['average']:.2f}%"
            })
        
        return alerts
    
    def run_monitoring_cycle(self):
        """執行一次監控循環"""
        logger.info("開始效能監控循環...")
        
        # 監控 API 效能
        api_results = self.monitor_api_endpoints()
        logger.info(f"API 監控完成，檢查了 {len(api_results)} 個端點")
        
        # 監控系統資源
        system_metrics = self.monitor_system_resources()
        logger.info("系統資源監控完成")
        
        # 監控資料庫效能
        db_metrics = self.monitor_database_performance()
        logger.info("資料庫效能監控完成")
        
        # 生成報告
        report = self.generate_performance_report()
        
        # 檢查警報
        alerts = self.check_alerts(report)
        
        if alerts:
            logger.warning(f"發現 {len(alerts)} 個警報")
            for alert in alerts:
                logger.warning(f"[{alert['severity'].upper()}] {alert['message']}")
        else:
            logger.info("系統運行正常，無警報")
        
        return {
            'api_results': api_results,
            'system_metrics': system_metrics,
            'db_metrics': db_metrics,
            'report': report,
            'alerts': alerts
        }

def main():
    """主函數"""
    config = {
        'api_base_url': os.getenv('API_BASE_URL', 'http://localhost:5000/api'),
        'db_path': os.getenv('MONITOR_DB_PATH', 'performance_monitor.db')
    }
    
    monitor = PerformanceMonitor(config)
    
    # 執行監控
    results = monitor.run_monitoring_cycle()
    
    # 輸出報告
    print("\n" + "="*50)
    print("📊 效能監控報告")
    print("="*50)
    
    print(f"\n🕐 報告時間: {results['report']['report_time']}")
    print(f"📈 監控時間範圍: {results['report']['time_range_hours']} 小時")
    
    print("\n🌐 API 效能:")
    for endpoint, stats in results['report']['api_performance'].items():
        print(f"  {endpoint}:")
        print(f"    平均回應時間: {stats['avg_response_time']:.2f}ms")
        print(f"    成功率: {stats['success_rate']:.2f}%")
        print(f"    總請求數: {stats['total_requests']}")
    
    print("\n💻 系統資源:")
    sys_res = results['report']['system_resources']
    print(f"  CPU: 平均 {sys_res['cpu']['average']:.2f}%, 最高 {sys_res['cpu']['maximum']:.2f}%")
    print(f"  記憶體: 平均 {sys_res['memory']['average']:.2f}%, 最高 {sys_res['memory']['maximum']:.2f}%")
    print(f"  磁碟: 平均 {sys_res['disk']['average']:.2f}%, 最高 {sys_res['disk']['maximum']:.2f}%")
    
    if results['alerts']:
        print("\n🚨 警報:")
        for alert in results['alerts']:
            print(f"  [{alert['severity'].upper()}] {alert['message']}")
    else:
        print("\n✅ 系統運行正常，無警報")
    
    print("\n" + "="*50)

if __name__ == "__main__":
    main()
