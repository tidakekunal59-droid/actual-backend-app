#!/bin/bash

# Ensure output directory exists
mkdir -p /logs/verifier/

fail() {
    echo "0" > /logs/verifier/reward.txt
    echo "Test Failed: $1"
    exit 0 # exit 0 so Harbor captures the score properly
}

pass() {
    echo "1" > /logs/verifier/reward.txt
    echo "All tests passed successfully."
    exit 0
}

echo "Running tests..."

# 1. Test Nginx Installation and Status
if ! dpkg -l | grep -q nginx; then
    fail "Nginx is not installed"
fi

if ! systemctl is-active --quiet nginx; then
    fail "Nginx is not running"
fi

if ! systemctl is-enabled --quiet nginx; then
    fail "Nginx is not enabled on boot"
fi

# 2. Test Custom Virtual Host
if [ ! -f /etc/nginx/sites-available/example.local ]; then
    fail "/etc/nginx/sites-available/example.local does not exist"
fi

if [ ! -L /etc/nginx/sites-enabled/example.local ]; then
    fail "Symlink /etc/nginx/sites-enabled/example.local does not exist"
fi

if [ -L /etc/nginx/sites-enabled/default ] || [ -f /etc/nginx/sites-enabled/default ]; then
    fail "Default nginx site is still enabled"
fi

if [ ! -f /var/www/example.local/html/index.html ]; then
    fail "index.html not found in /var/www/example.local/html"
fi

INDEX_CONTENT=$(cat /var/www/example.local/html/index.html)
if [ "$INDEX_CONTENT" != "Welcome to example.local!" ]; then
    fail "index.html content is incorrect. Expected 'Welcome to example.local!', got '$INDEX_CONTENT'"
fi

# Test Nginx serves the file (modify hosts to test locally)
echo "127.0.0.1 example.local" >> /etc/hosts
RESPONSE=$(curl -s http://example.local)
if [ "$RESPONSE" != "Welcome to example.local!" ]; then
    fail "Nginx is not serving the expected content for example.local on port 80"
fi

# 3. Test Firewall (UFW)
if ! dpkg -l | grep -q ufw; then
    fail "UFW is not installed"
fi

UFW_STATUS=$(ufw status verbose)
if ! echo "$UFW_STATUS" | grep -q "Status: active"; then
    fail "UFW is not active"
fi

if ! echo "$UFW_STATUS" | grep -q "Default: deny (incoming), allow (outgoing)"; then
    fail "UFW default policies are incorrect"
fi

if ! echo "$UFW_STATUS" | grep -E "80/tcp.*ALLOW IN"; then
    fail "UFW is not allowing port 80"
fi

if ! echo "$UFW_STATUS" | grep -E "22/tcp.*ALLOW IN"; then
    fail "UFW is not allowing port 22"
fi

# 4. Test Sudo User
if ! id "sysadmin" >/dev/null 2>&1; then
    fail "User 'sysadmin' does not exist"
fi

if ! groups sysadmin | grep -q "\bsudo\b"; then
    fail "User 'sysadmin' is not in the 'sudo' group"
fi

# 5. Test Custom Systemd Service
if [ ! -f /usr/local/bin/dummy_service.sh ]; then
    fail "/usr/local/bin/dummy_service.sh does not exist"
fi

if [ ! -x /usr/local/bin/dummy_service.sh ]; then
    fail "/usr/local/bin/dummy_service.sh is not executable"
fi

if [ ! -f /etc/systemd/system/dummy.service ]; then
    fail "dummy.service file does not exist"
fi

if ! systemctl is-active --quiet dummy.service; then
    fail "dummy.service is not running"
fi

if ! systemctl is-enabled --quiet dummy.service; then
    fail "dummy.service is not enabled on boot"
fi

# 6. Test Cron Job
if [ ! -d /backup ]; then
    fail "/backup directory does not exist"
fi

CRON_CMD=$(crontab -l -u root 2>/dev/null | grep "^0 2 \* \* \*") || true

if [ -z "$CRON_CMD" ]; then
    fail "Cron job is not scheduled for 2:00 AM"
fi

if ! echo "$CRON_CMD" | grep -q "tar"; then
    fail "Cron job does not use 'tar'"
fi

if ! echo "$CRON_CMD" | grep -q "/backup/www_backup.tar.gz"; then
    fail "Cron job does not output to /backup/www_backup.tar.gz"
fi

if ! echo "$CRON_CMD" | grep -q "example.local"; then
    fail "Cron job does not back up example.local files"
fi

# All checks passed
pass
