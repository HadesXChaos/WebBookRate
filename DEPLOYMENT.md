# Production Deployment Guide

Hướng dẫn triển khai BookReview.vn lên môi trường production.

## Yêu cầu

- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Nginx
- Gunicorn
- Docker & Docker Compose (khuyến nghị)
- SSL Certificate (Let's Encrypt)

## 1. Chuẩn bị môi trường

### 1.1 Cấu hình biến môi trường

Tạo file `.env` trong thư mục dự án:

```bash
# Django Settings
DEBUG=False
SECRET_KEY=your-secret-key-here-change-in-production
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
BASE_URL=https://yourdomain.com

# Database
DB_NAME=bookreview_prod
DB_USER=bookreview_user
DB_PASSWORD=strong-password-here
DB_HOST=localhost
DB_PORT=5432

# Redis
REDIS_URL=redis://localhost:6379/0

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com

# AWS S3 (hoặc MinIO)
USE_S3=True
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=bookreview-media
AWS_S3_ENDPOINT_URL=https://s3.amazonaws.com
AWS_S3_REGION_NAME=us-east-1
AWS_S3_CUSTOM_DOMAIN=cdn.yourdomain.com

# CORS
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Security
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### 1.2 Tạo Secret Key

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## 2. Cài đặt Database

### 2.1 PostgreSQL

```bash
# Tạo database và user
sudo -u postgres psql
CREATE DATABASE bookreview_prod;
CREATE USER bookreview_user WITH PASSWORD 'strong-password-here';
ALTER ROLE bookreview_user SET client_encoding TO 'utf8';
ALTER ROLE bookreview_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE bookreview_user SET timezone TO 'Asia/Ho_Chi_Minh';
GRANT ALL PRIVILEGES ON DATABASE bookreview_prod TO bookreview_user;
\q
```

### 2.2 Chạy migrations

```bash
python manage.py migrate
```

## 3. Tạo Superuser

```bash
python manage.py createsuperuser
```

## 4. Thu thập Static Files

```bash
python manage.py collectstatic --noinput
```

## 5. Cấu hình Gunicorn

### 5.1 Cài đặt Gunicorn

```bash
pip install gunicorn
```

### 5.2 Tạo file `gunicorn_config.py`

```python
import multiprocessing

bind = "127.0.0.1:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
timeout = 30
keepalive = 2
max_requests = 1000
max_requests_jitter = 50
```

### 5.3 Tạo systemd service

Tạo file `/etc/systemd/system/bookreview.service`:

```ini
[Unit]
Description=BookReview Gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/bookreview
ExecStart=/path/to/venv/bin/gunicorn \
    --config /path/to/bookreview/gunicorn_config.py \
    bookreview.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
```

Khởi động service:

```bash
sudo systemctl daemon-reload
sudo systemctl start bookreview
sudo systemctl enable bookreview
```

## 6. Cấu hình Nginx

### 6.1 Tạo file cấu hình Nginx

Tạo file `/etc/nginx/sites-available/bookreview`:

```nginx
upstream bookreview {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;
    
    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    # Security Headers
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    
    # Logging
    access_log /var/log/nginx/bookreview_access.log;
    error_log /var/log/nginx/bookreview_error.log;
    
    # Static Files
    location /static/ {
        alias /path/to/bookreview/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    # Media Files (if using local storage)
    location /media/ {
        alias /path/to/bookreview/media/;
        expires 7d;
        add_header Cache-Control "public";
    }
    
    # Proxy to Gunicorn
    location / {
        proxy_pass http://bookreview;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    # Health check
    location /healthz {
        proxy_pass http://bookreview;
        access_log off;
    }
}
```

### 6.2 Kích hoạt site

```bash
sudo ln -s /etc/nginx/sites-available/bookreview /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## 7. SSL Certificate (Let's Encrypt)

```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

Certbot sẽ tự động cấu hình Nginx và gia hạn certificate.

## 8. Cấu hình Celery

### 8.1 Tạo systemd service cho Celery Worker

Tạo file `/etc/systemd/system/celery-worker.service`:

```ini
[Unit]
Description=Celery Worker for BookReview
After=network.target

[Service]
Type=forking
User=www-data
Group=www-data
WorkingDirectory=/path/to/bookreview
EnvironmentFile=/path/to/bookreview/.env
ExecStart=/path/to/venv/bin/celery -A bookreview worker \
    --loglevel=info \
    --logfile=/var/log/celery/worker.log \
    --pidfile=/var/run/celery/worker.pid \
    --detach
ExecStop=/bin/kill -s TERM $MAINPID
Restart=always

[Install]
WantedBy=multi-user.target
```

### 8.2 Tạo systemd service cho Celery Beat

Tạo file `/etc/systemd/system/celery-beat.service`:

```ini
[Unit]
Description=Celery Beat for BookReview
After=network.target

[Service]
Type=forking
User=www-data
Group=www-data
WorkingDirectory=/path/to/bookreview
EnvironmentFile=/path/to/bookreview/.env
ExecStart=/path/to/venv/bin/celery -A bookreview beat \
    --loglevel=info \
    --logfile=/var/log/celery/beat.log \
    --pidfile=/var/run/celery/beat.pid \
    --detach
ExecStop=/bin/kill -s TERM $MAINPID
Restart=always

[Install]
WantedBy=multi-user.target
```

Khởi động services:

```bash
sudo systemctl daemon-reload
sudo systemctl start celery-worker
sudo systemctl start celery-beat
sudo systemctl enable celery-worker
sudo systemctl enable celery-beat
```

## 9. Cấu hình Redis

### 9.1 Cài đặt Redis

```bash
sudo apt-get install redis-server
```

### 9.2 Cấu hình Redis

Chỉnh sửa `/etc/redis/redis.conf`:

```
bind 127.0.0.1
requirepass your-redis-password
maxmemory 256mb
maxmemory-policy allkeys-lru
```

Khởi động lại Redis:

```bash
sudo systemctl restart redis-server
```

## 10. Monitoring & Logging

### 10.1 Cấu hình Log Rotation

Tạo file `/etc/logrotate.d/bookreview`:

```
/var/log/bookreview/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    sharedscripts
    postrotate
        systemctl reload bookreview > /dev/null 2>&1 || true
    endscript
}
```

### 10.2 Sentry (Optional)

Thêm vào `requirements.txt`:

```
sentry-sdk==1.38.0
```

Cấu hình trong `settings.py`:

```python
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[DjangoIntegration()],
    traces_sample_rate=0.1,
    send_default_pii=True
)
```

## 11. Backup

### 11.1 Database Backup Script

Tạo file `/usr/local/bin/backup-bookreview.sh`:

```bash
#!/bin/bash
BACKUP_DIR="/backup/bookreview"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

# Database backup
pg_dump -U bookreview_user bookreview_prod | gzip > $BACKUP_DIR/db_$DATE.sql.gz

# Media files backup (if using local storage)
tar -czf $BACKUP_DIR/media_$DATE.tar.gz /path/to/bookreview/media/

# Keep only last 7 days
find $BACKUP_DIR -type f -mtime +7 -delete
```

Thêm vào crontab:

```bash
0 2 * * * /usr/local/bin/backup-bookreview.sh
```

## 12. Deployment Checklist

- [ ] Cấu hình biến môi trường
- [ ] Tạo database và user
- [ ] Chạy migrations
- [ ] Tạo superuser
- [ ] Thu thập static files
- [ ] Cấu hình Gunicorn
- [ ] Cấu hình Nginx
- [ ] Cài đặt SSL certificate
- [ ] Cấu hình Celery worker và beat
- [ ] Cấu hình Redis
- [ ] Thiết lập monitoring
- [ ] Thiết lập backup
- [ ] Kiểm tra tất cả endpoints
- [ ] Kiểm tra email sending
- [ ] Kiểm tra file uploads
- [ ] Kiểm tra cache hoạt động
- [ ] Kiểm tra Celery tasks

## 13. Troubleshooting

### 13.1 Kiểm tra logs

```bash
# Django logs
sudo journalctl -u bookreview -f

# Nginx logs
sudo tail -f /var/log/nginx/bookreview_error.log

# Celery logs
sudo tail -f /var/log/celery/worker.log
```

### 13.2 Kiểm tra services

```bash
sudo systemctl status bookreview
sudo systemctl status celery-worker
sudo systemctl status celery-beat
sudo systemctl status nginx
sudo systemctl status redis-server
```

### 13.3 Kiểm tra database connection

```bash
python manage.py dbshell
```

### 13.4 Kiểm tra Redis connection

```bash
redis-cli -a your-redis-password ping
```

## 14. Performance Optimization

### 14.1 Database Indexes

Đảm bảo tất cả indexes đã được tạo:

```bash
python manage.py sqlmigrate books 0001
python manage.py sqlmigrate reviews 0001
```

### 14.2 Cache Configuration

Kiểm tra Redis cache hoạt động:

```bash
python manage.py shell
>>> from django.core.cache import cache
>>> cache.set('test', 'value')
>>> cache.get('test')
```

### 14.3 Static Files CDN

Cấu hình CDN cho static files trong `settings.py`:

```python
STATIC_URL = 'https://cdn.yourdomain.com/static/'
```

## 15. Security Checklist

- [ ] DEBUG=False
- [ ] SECRET_KEY được bảo mật
- [ ] ALLOWED_HOSTS được cấu hình đúng
- [ ] SSL/TLS được cấu hình
- [ ] Security headers được thiết lập
- [ ] Database password mạnh
- [ ] Redis password được thiết lập
- [ ] File permissions được cấu hình đúng
- [ ] Firewall rules được thiết lập
- [ ] Regular security updates

## 16. Maintenance

### 16.1 Cập nhật code

```bash
cd /path/to/bookreview
git pull
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart bookreview
```

### 16.2 Database migrations

```bash
python manage.py migrate
```

### 16.3 Clear cache

```bash
python manage.py shell
>>> from django.core.cache import cache
>>> cache.clear()
```

## 17. Docker Deployment (Alternative)

Nếu sử dụng Docker, cập nhật `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  web:
    build: .
    command: gunicorn bookreview.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - ./staticfiles:/app/staticfiles
      - ./media:/app/media
    env_file:
      - .env
    depends_on:
      - db
      - redis

  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data
    env_file:
      - .env

  redis:
    image: redis:7-alpine
    command: redis-server --requirepass ${REDIS_PASSWORD}

  celery:
    build: .
    command: celery -A bookreview worker -l info
    env_file:
      - .env
    depends_on:
      - db
      - redis

  celery-beat:
    build: .
    command: celery -A bookreview beat -l info
    env_file:
      - .env
    depends_on:
      - db
      - redis

volumes:
  postgres_data:
```

Khởi động:

```bash
docker-compose -f docker-compose.prod.yml up -d
```

---

**Lưu ý:** Thay thế tất cả các giá trị placeholder (yourdomain.com, paths, passwords) bằng giá trị thực tế của bạn.

