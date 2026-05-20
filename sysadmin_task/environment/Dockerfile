FROM ubuntu:22.04

# Avoid tzdata interactive prompts during package installations
ENV DEBIAN_FRONTEND=noninteractive

# Update and install some baseline utilities that might be expected
# like curl, systemd (often needed for full sysadmin tests, though docker
# requires special handling for systemd, we will install it just in case),
# sudo, and cron.
RUN apt-get update && apt-get install -y \
    curl \
    sudo \
    cron \
    systemd \
    systemd-sysv \
    iptables \
    ufw \
    nginx \
    python3 \
    python3-pytest \
    && rm -rf /var/lib/apt/lists/*

# Mask some systemd services that don't make sense in a container
RUN systemctl mask dev-mqueue.mount dev-hugepages.mount \
    sys-fs-fuse-connections.mount sys-kernel-config.mount \
    sys-kernel-debug.mount sys-kernel-tracing.mount \
    display-manager.service \
    systemd-hwdb-update.service \
    systemd-journald-audit.socket \
    systemd-networkd.socket \
    systemd-networkd \
    systemd-resolved

# Remove default nginx to ensure it starts fresh
RUN apt-get update && apt-get purge -y nginx nginx-common && apt-get autoremove -y

# Revert DEBIAN_FRONTEND
ENV DEBIAN_FRONTEND=dialog

# Set systemd as the entrypoint to allow starting services like nginx and custom ones
# NOTE: Running systemd in docker usually requires --privileged or specific volume mounts
# Harbor will need to run the container appropriately, but this sets up the image correctly.
STOPSIGNAL SIGRTMIN+3
CMD ["/sbin/init"]
