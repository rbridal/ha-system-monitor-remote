# HA System Monitor Remote

Home Assistant integration for a host running [system-monitor-remote](https://github.com/rbridal/system-monitor-remote).

Same sensors as the enabled System Monitor set on shop-ha: disk usage `/`, memory usage, processor use, processor temperature, load 1/5/15, uptime, IPv4 per interface, and fan speed when the host has one.

Domain `system_monitor_remote`, so it sits next to the built-in `systemmonitor` integration. One config entry per host. `shop-*` entries belong on shop-ha. `home-*` entries belong on home-ha.
