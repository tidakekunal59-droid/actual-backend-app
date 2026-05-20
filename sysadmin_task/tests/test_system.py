import subprocess
import os

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result

def test_nginx_installation_and_status():
    assert run_cmd("dpkg -l | grep -q nginx").returncode == 0, "Nginx is not installed"
    assert run_cmd("systemctl is-active --quiet nginx").returncode == 0, "Nginx is not running"
    assert run_cmd("systemctl is-enabled --quiet nginx").returncode == 0, "Nginx is not enabled on boot"

def test_custom_virtual_host():
    assert os.path.exists("/etc/nginx/sites-available/example.local"), "/etc/nginx/sites-available/example.local does not exist"
    assert os.path.islink("/etc/nginx/sites-enabled/example.local"), "Symlink /etc/nginx/sites-enabled/example.local does not exist"
    assert not (os.path.islink("/etc/nginx/sites-enabled/default") or os.path.exists("/etc/nginx/sites-enabled/default")), "Default nginx site is still enabled"

    index_path = "/var/www/example.local/html/index.html"
    assert os.path.exists(index_path), "index.html not found in /var/www/example.local/html"

    with open(index_path, "r") as f:
        content = f.read().strip()
    assert content == "Welcome to example.local!", f"index.html content is incorrect. Got '{content}'"

    # Test Nginx serves the file (local test assuming /etc/hosts modification)
    run_cmd('echo "127.0.0.1 example.local" >> /etc/hosts')
    res = run_cmd("curl -s http://example.local")
    assert res.stdout.strip() == "Welcome to example.local!", "Nginx is not serving the expected content for example.local on port 80"

def test_firewall_ufw():
    assert run_cmd("dpkg -l | grep -q ufw").returncode == 0, "UFW is not installed"

    ufw_status = run_cmd("ufw status verbose").stdout
    assert "Status: active" in ufw_status, "UFW is not active"
    assert "Default: deny (incoming), allow (outgoing)" in ufw_status, "UFW default policies are incorrect"

    import re
    assert re.search(r"80/tcp.*ALLOW IN", ufw_status), "UFW is not allowing port 80"
    assert re.search(r"22/tcp.*ALLOW IN", ufw_status), "UFW is not allowing port 22"

def test_sudo_user():
    assert run_cmd("id sysadmin").returncode == 0, "User 'sysadmin' does not exist"
    assert "sudo" in run_cmd("groups sysadmin").stdout.split(), "User 'sysadmin' is not in the 'sudo' group"

def test_custom_systemd_service():
    script_path = "/usr/local/bin/dummy_service.sh"
    assert os.path.exists(script_path), f"{script_path} does not exist"
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable"
    assert os.path.exists("/etc/systemd/system/dummy.service"), "dummy.service file does not exist"

    assert run_cmd("systemctl is-active --quiet dummy.service").returncode == 0, "dummy.service is not running"
    assert run_cmd("systemctl is-enabled --quiet dummy.service").returncode == 0, "dummy.service is not enabled on boot"

def test_cron_job():
    assert os.path.isdir("/backup"), "/backup directory does not exist"

    cron_cmd = run_cmd("crontab -l -u root 2>/dev/null | grep '^0 2 \* \* \*'").stdout.strip()
    assert cron_cmd, "Cron job is not scheduled for 2:00 AM"
    assert "tar" in cron_cmd, "Cron job does not use 'tar'"
    assert "/backup/www_backup.tar.gz" in cron_cmd, "Cron job does not output to /backup/www_backup.tar.gz"
    assert "example.local" in cron_cmd, "Cron job does not back up example.local files"
