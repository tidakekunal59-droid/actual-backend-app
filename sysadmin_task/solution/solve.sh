#!/bin/bash

# Exit on error
set -e

echo "Starting solution script..."

# 1. Install and Start Nginx
echo "Installing Nginx..."
apt-get update
apt-get install -y nginx

echo "Starting Nginx..."
systemctl start nginx
systemctl enable nginx

# 2. Configure a Custom Virtual Host
echo "Configuring Custom Virtual Host..."
mkdir -p /var/www/example.local/html
echo "Welcome to example.local!" > /var/www/example.local/html/index.html

cat << 'EOF' > /etc/nginx/sites-available/example.local
server {
    listen 80;
    server_name example.local;

    root /var/www/example.local/html;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}
EOF

ln -sf /etc/nginx/sites-available/example.local /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
systemctl reload nginx

# 3. Configure Firewall (UFW)
echo "Configuring UFW..."
apt-get install -y ufw
# In docker, ufw might complain about iptables/ipv6, forcing it
ufw --force reset
ufw default deny incoming
ufw default allow outgoing
ufw allow 80/tcp
ufw allow 22/tcp
# Enable UFW without prompting
ufw --force enable

# 4. Create a Sudo User
echo "Creating Sudo User..."
useradd -m -s /bin/bash sysadmin
echo "sysadmin:P@ssw0rd123!" | chpasswd
usermod -aG sudo sysadmin

# 5. Write a Custom Systemd Service
echo "Writing Custom Systemd Service..."
cat << 'EOF' > /usr/local/bin/dummy_service.sh
#!/bin/bash
while true; do
    echo "$(date): Dummy service is running" >> /var/log/dummy_service.log
    sleep 10
done
EOF
chmod +x /usr/local/bin/dummy_service.sh

cat << 'EOF' > /etc/systemd/system/dummy.service
[Unit]
Description=Dummy Service
After=network.target

[Service]
Type=simple
ExecStart=/usr/local/bin/dummy_service.sh
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable dummy.service
systemctl start dummy.service

# 6. Set up a Cron Job for Backups
echo "Setting up Cron Job..."
mkdir -p /backup
# Add cron job for root. Note: The crontab file needs a newline at the end.
(crontab -l 2>/dev/null || true; echo "0 2 * * * tar -czf /backup/www_backup.tar.gz -C /var/www/example.local html") | crontab -

echo "Solution script completed successfully."
