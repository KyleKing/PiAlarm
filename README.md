# PiAlarm
Turn on LEDs, motors, etc. with Node, Cron, React, etc!


[Based on React example apps published by Twilio](https://www.twilio.com/blog/2015/08/setting-up-react-for-es6-with-webpack-and-babel-2.html)


## Port Forwarding:

> Add sudo nano /etc/dhcpcd.conf:
```
interface wlan0

static ip_address=192.168.0.106/24
static routers=192.168.0.1
static domain_name_servers=192.168.0.1
```

> Add /etc/rc.local:
```
# Forward port 80 to 3000, so the web server can run with normal permissions
iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 3000
```

Then under 'Forwarding' -> 'Virtual Servers' create:

Service Port (80 - http)
Internal Port (leave blank to match service port)
IP Address (192.168.0.106)
Protocol (TCP)

Google `what is my ip` and copy that number into your browser

[Add port 22 if you want remote ssh access...although probably not wise]


## TODO

- Consider adding a button that sets an alarm to go off at 8 hours from that moment. Would need to stop all alarms and store the pointers in an array, then a cron task running each night would have to restart them