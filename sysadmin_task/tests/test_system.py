import subprocess
import os

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and ("Permission denied" in result.stderr or "must be root" in result.stderr or "Operation not permitted" in result.stderr or "Permission denied" in result.stdout):
        result = subprocess.run(f"sudo bash -c \"{cmd}\"", shell=True, capture_output=True, text=True)

    if result.stdout.strip() == "" and result.returncode != 0:
        result2 = subprocess.run(f"sudo bash -c \"{cmd}\"", shell=True, capture_output=True, text=True)
        if result2.returncode == 0 or result2.stdout.strip() != "":
            return result2
    return result

def test_nginx_installation_and_status():
    assert run_cmd("dpkg -l | grep -q nginx").returncode == 0, "Nginx is not installed"

    is_active = run_cmd("systemctl is-active --quiet nginx").returncode == 0
    is_enabled = run_cmd("systemctl is-enabled --quiet nginx").returncode == 0
    assert is_active or is_enabled, "Nginx is neither running nor enabled"

def test_custom_virtual_host():
    assert os.path.exists("/etc/nginx/sites-available/example.local"), "/etc/nginx/sites-available/example.local does not exist"
    assert os.path.islink("/etc/nginx/sites-enabled/example.local"), "Symlink /etc/nginx/sites-enabled/example.local does not exist"
    assert not (os.path.islink("/etc/nginx/sites-enabled/default") or os.path.exists("/etc/nginx/sites-enabled/default")), "Default nginx site is still enabled"

    index_path = "/var/www/example.local/html/index.html"
    assert os.path.exists(index_path), "index.html not found in /var/www/example.local/html"

    with open(index_path, "r") as f:
        content = f.read().strip()
    assert content == "Welcome to example.local!", f"index.html content is incorrect. Got '{content}'"

    if run_cmd("systemctl is-active --quiet nginx").returncode == 0:
        res = run_cmd('curl -s -H "Host: example.local" http://127.0.0.1')
        assert res.stdout.strip() == "Welcome to example.local!", "Nginx is not serving the expected content for example.local on port 80"

def test_firewall_ufw():
    assert run_cmd("dpkg -l | grep -q ufw").returncode == 0, "UFW is not installed"

    ufw_conf = run_cmd("cat /etc/ufw/ufw.conf 2>/dev/null").stdout
    assert "ENABLED=yes" in ufw_conf, "UFW is not configured to be enabled"

    ufw_default = run_cmd("cat /etc/default/ufw 2>/dev/null").stdout
    assert "DEFAULT_INPUT_POLICY=\"DROP\"" in ufw_default or "DEFAULT_INPUT_POLICY=\"DENY\"" in ufw_default, "UFW default incoming policy is incorrect"
    assert "DEFAULT_OUTPUT_POLICY=\"ACCEPT\"" in ufw_default or "DEFAULT_OUTPUT_POLICY=\"ALLOW\"" in ufw_default, "UFW default outgoing policy is incorrect"

    # We rely on checking ENABLED=yes and the default policies in ufw.conf / default/ufw,
    # as specific port rules fail to write in Docker environments lacking proper kernel capabilities.

def test_sudo_user():
    assert run_cmd("id sysadmin").returncode == 0, "User 'sysadmin' does not exist"
    assert "sudo" in run_cmd("groups sysadmin").stdout.split(), "User 'sysadmin' is not in the 'sudo' group"

def test_custom_systemd_service():
    script_path = "/usr/local/bin/dummy_service.sh"
    assert os.path.exists(script_path), f"{script_path} does not exist"
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable"
    assert os.path.exists("/etc/systemd/system/dummy.service"), "dummy.service file does not exist"

    is_enabled = run_cmd("systemctl is-enabled --quiet dummy.service").returncode == 0
    service_content = run_cmd("cat /etc/systemd/system/dummy.service").stdout
    has_exec = "ExecStart=/usr/local/bin/dummy_service.sh" in service_content

    assert is_enabled and has_exec, "dummy.service is not configured correctly or not enabled"

def test_cron_job():
    assert os.path.isdir("/backup"), "/backup directory does not exist"

    cron_cmd = run_cmd("crontab -l -u root 2>/dev/null").stdout.strip()
    assert "0 2" in cron_cmd or "00 2" in cron_cmd or "0 02" in cron_cmd, "Cron job is not scheduled for 2:00 AM"
    assert "tar" in cron_cmd, "Cron job does not use 'tar'"
    assert "/backup/www_backup.tar.gz" in cron_cmd, "Cron job does not output to /backup/www_backup.tar.gz"
    assert "example.local" in cron_cmd, "Cron job does not back up example.local files"
