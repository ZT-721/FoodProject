# Stage 1: Build/Install Dependencies
FROM python:3.11-slim as backend-build

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    # Clean up APT when done
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements file first to leverage caching
COPY backend/requirements.txt .




# Install python dependencies
RUN pip install --no-cache-dir -r requirements.txt


# Stage 2: Production Image
FROM python:3.11-slim as backend-run

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Copy installed dependencies and application code from the build stage
COPY --from=backend-build /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# 拷執行檔（關鍵！）
COPY --from=backend-build /usr/local/bin /usr/local/bin
COPY backend/ .

# Expose port (optional, but good practice)
EXPOSE 5000
# 驗證 gunicorn 是否存在
RUN which gunicorn && echo "gunicorn found at $(which gunicorn)" || (echo "gunicorn MISSING!" && exit 1)

# Command to run the application using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
