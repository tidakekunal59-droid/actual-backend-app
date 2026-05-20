# Comprehensive System Administration Task

Your goal is to perform a series of standard system administration tasks to configure this Ubuntu server. You have root access. Complete the following 6 system-wide objectives.

## Objectives

1. **Install and Start Nginx**
   - Install the `nginx` package.
   - Ensure the `nginx` service is running and enabled to start on boot.

2. **Configure a Custom Virtual Host**
   - Create a new virtual host configuration for `example.local` in `/etc/nginx/sites-available/example.local`.
   - The virtual host should serve static files from `/var/www/example.local/html`.
   - Create the directory `/var/www/example.local/html` and add an `index.html` file containing the exact string `Welcome to example.local!`.
   - Create a symlink in `/etc/nginx/sites-enabled/` to enable this virtual host.
   - The virtual host should listen on port `80` for the server name `example.local`.
   - Ensure the default nginx site is disabled (remove the symlink `/etc/nginx/sites-enabled/default`).
   - Reload or restart Nginx to apply changes.

3. **Configure Firewall (UFW)**
   - Install `ufw` if it's not already installed.
   - Enable `ufw`.
   - Allow incoming connections on port `80` (HTTP).
   - Allow incoming connections on port `22` (SSH).
   - Set the default incoming policy to `deny` and default outgoing policy to `allow`.

4. **Create a Sudo User**
   - Create a new user named `sysadmin`.
   - Set the user's password to `P@ssw0rd123!` (or disable password login, but ensure the user exists). *For testing purposes, simply creating the user and adding them to the correct group is sufficient.*
   - Add the `sysadmin` user to the `sudo` group so they have root privileges.

5. **Write a Custom Systemd Service**
   - Create a script at `/usr/local/bin/dummy_service.sh` that appends the current date and the string `Dummy service is running` to `/var/log/dummy_service.log` every 10 seconds. Make sure the script is executable.
   - Create a systemd service file at `/etc/systemd/system/dummy.service` that runs this script.
   - Start the `dummy.service` and enable it to start on boot.

6. **Set up a Cron Job for Backups**
   - Create a cron job for the `root` user that creates a tar.gz archive of the `/var/www/example.local/html` directory.
   - The archive should be saved to `/backup/www_backup.tar.gz`.
   - The cron job should run every day at 2:00 AM.
   - You must create the `/backup` directory.
