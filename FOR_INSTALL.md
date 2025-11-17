# VPS Installation Guide

## 1. Prepare the server
1. Connect via SSH: `ssh user@your-vps`
2. Update OS and install Docker + Compose:
   ```bash
   sudo apt update && sudo apt upgrade -y
   curl -fsSL https://get.docker.com | sudo sh
   sudo usermod -aG docker $USER
   exit   # reconnect so group membership applies
   ```
3. Install nginx & firewall rules:
   ```bash
   sudo apt install -y nginx
   sudo ufw allow 'Nginx Full'
   sudo ufw enable
   ```

## 2. Get the project
```bash
git clone https://github.com/Meatxboy/eduquest eduquest
cd eduquest
```

## 3. Configure environment
1. Copy env templates:
   ```bash
   cp backend/.env.example backend/.env
   cp bot/.env.example bot/.env
   cp frontend/.env.example frontend/.env
   ```
2. Edit files (`nano path/.env`) and set real values:
   - `backend/.env`: `ENVIRONMENT=production`, `DATABASE_URL=postgresql+asyncpg://postgres:postgres@postgres:5432/eduquest`, `REDIS_URL=redis://redis:6379/0`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_WEBHOOK_SECRET`, `CORS_ORIGINS=https://tu-tor.ai-gruzdev.ru`.
   - `bot/.env`: same bot token/secret, `BACKEND_BASE_URL=https://tu-tor.ai-gruzdev.ru/api`, `FRONTEND_BASE_URL=https://tu-tor.ai-gruzdev.ru`, `WEBHOOK_URL=https://tu-tor.ai-gruzdev.ru/telegram/webhook`, `REDIS_URL=redis://redis:6379/1`.
   - `frontend/.env`: `VITE_BACKEND_URL=https://tu-tor.ai-gruzdev.ru/api`, `VITE_TELEGRAM_BOT_NAME=@your_bot`.
3. Root `.env` (used by Compose):
   ```bash
   cat > .env <<'EOV'
   TELEGRAM_BOT_TOKEN=8092405...MCXk
   TELEGRAM_WEBHOOK_SECRET=super-secret
   TELEGRAM_BOT_NAME=tu_tor_bot
   FRONTEND_BASE_URL=https://tu-tor.ai-gruzdev.ru
   EOV
   ```
4. Lock down published ports in `docker-compose.yml`:
   ```yaml
   backend:
     ports: ["127.0.0.1:8000:8000"]
   bot:
     ports: ["127.0.0.1:8081:8081"]
   frontend:
     ports: ["127.0.0.1:4173:80"]
   ```

## 4. nginx reverse proxy + HTTPS
1. Create site config `/etc/nginx/sites-available/tu-tor.ai-gruzdev.ru`:
   ```nginx
   server {
       listen 80;
       listen [::]:80;
       server_name tu-tor.ai-gruzdev.ru;
       return 301 https://$host$request_uri;
   }

   server {
       listen 443 ssl http2;
       listen [::]:443 ssl http2;
       server_name tu-tor.ai-gruzdev.ru;

       ssl_certificate /etc/letsencrypt/live/tu-tor.ai-gruzdev.ru/fullchain.pem;
       ssl_certificate_key /etc/letsencrypt/live/tu-tor.ai-grузdev.ru/privkey.pem;
       include /etc/letsencrypt/options-ssl-nginx.conf;
       ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

       location /api/ { proxy_pass http://127.0.0.1:8000/; include proxy_params; }
       location = /telegram/webhook { proxy_pass http://127.0.0.1:8081/webhook; include proxy_params; }
       location / { proxy_pass http://127.0.0.1:4173; include proxy_params; }
   }
   ```
2. Enable the site:
   ```bash
   sudo ln -s /etc/nginx/sites-available/tu-tor.ai-gruzdev.ru /etc/nginx/sites-enabled/
   sudo rm -f /etc/nginx/sites-enabled/default
   sudo nginx -t && sudo systemctl reload nginx
   ```
3. Install Certbot + certificates:
   ```bash
   sudo snap install --classic certbot
   sudo ln -s /snap/bin/certbot /usr/bin/certbot
   sudo certbot --nginx -d tu-tor.ai-gruzdev.ru
   ```
   Certbot updates the config with valid SSL paths.

## 5. Launch the stack
```bash
docker compose up -d --build
docker compose ps
```
Checks:
```bash
curl -I https://tu-tor.ai-gruzdev.ru/api/health
curl -I https://tu-tor.ai-gruzdev.ru
curl https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getWebhookInfo
```

## 6. Seed data (optional)
```bash
docker compose exec -T postgres psql -U postgres -d eduquest < infra/seed.sql
```

## 7. Backups
- PostgreSQL: `docker compose exec -T postgres pg_dump -U postgres eduquest > backup.sql`
- Redis dump: `docker compose exec redis redis-cli save && docker compose cp redis:/data/dump.rdb ./redis_dump.rdb`
- Copy `.env` and nginx config to safe storage.

## 8. Updates
```bash
git pull
docker compose up -d --build
sudo certbot renew --dry-run   # periodic TLS refresh
```
