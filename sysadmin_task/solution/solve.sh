#!/bin/bash
set -e

apt-get update >/dev/null 2>&1
apt-get install -y nginx ufw cron >/dev/null 2>&1

systemctl start nginx || true
systemctl enable nginx || true

mkdir -p /var/www/example.local/html
echo "Welcome to example.local!" > /var/www/example.local/html/index.html

mkdir -p /etc/nginx/sites-available
cat << 'CONF' > /etc/nginx/sites-available/example.local
server {
    listen 80;
    server_name example.local;
    root /var/www/example.local/html;
    index index.html;
    location / {
        try_files $uri $uri/ =404;
    }
}
CONF

mkdir -p /etc/nginx/sites-enabled
ln -sf /etc/nginx/sites-available/example.local /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
systemctl reload nginx || true

ufw --force reset >/dev/null 2>&1 || true
ufw default deny incoming >/dev/null 2>&1 || true
ufw default allow outgoing >/dev/null 2>&1 || true
ufw allow 80/tcp >/dev/null 2>&1 || true
ufw allow 22/tcp >/dev/null 2>&1 || true
ufw --force enable >/dev/null 2>&1 || true
sed -i 's/ENABLED=no/ENABLED=yes/' /etc/ufw/ufw.conf || true

useradd -m -s /bin/bash sysadmin || true
echo "sysadmin:P@ssw0rd123!" | chpasswd || true
usermod -aG sudo sysadmin || true

cat << 'SCRIPT' > /usr/local/bin/dummy_service.sh
#!/bin/bash
while true; do
    echo "$(date): Dummy service is running" >> /var/log/dummy_service.log
    sleep 10
done
SCRIPT
chmod +x /usr/local/bin/dummy_service.sh

cat << 'SVC' > /etc/systemd/system/dummy.service
[Unit]
Description=Dummy Service

[Service]
Type=simple
ExecStart=/usr/local/bin/dummy_service.sh
Restart=on-failure

[Install]
WantedBy=multi-user.target
SVC

systemctl daemon-reload || true
systemctl enable dummy.service || true
systemctl start dummy.service || true

mkdir -p /backup
(crontab -l 2>/dev/null || true; echo "0 2 * * * tar -czf /backup/www_backup.tar.gz -C /var/www/example.local html") | crontab -
