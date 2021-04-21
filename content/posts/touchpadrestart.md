+++
title = "[FIX] ELan touchpad stops working at boot"
description = ""
tags = [
	"Arch Linux",
	"Linux",
	"Tech",
	"technology",
	"unix"
]
date = "2021-03-24"
categories = [
    "Tech",
    "Linux",
    "Fix"
]
images = []
+++

There was this issue that I faced in my system **(HP Pavilion Gaming 15 Laptop)** in which the touchpad **(ElanTech)** would stop working when the laptop booted, the fix to which was to move my finger on the touchpad when the system was booting up. Doing this every time was not convenient, so it took me a while, but this is what I did.

Create a script, called ```touchpadrestart.sh``` and put the below code in it.

```
#!/bin/sh
rmmod i2c_hid && modprobe i2c_hid
```
What the code does is, it disables the driver for the touchpad, and then enables it again. Put this in the path and run it whenever you need your touchpad to start working again. But this solution itself is not very efficient as it needs root access to run. We can make the process more streamlined by turning this into a systemd service.

First create the file ```/etc/systemd/system/touchpadrestart.service```. After that, make sure the path in ExecStart has the same command as out script.


```
[Unit]
Description=TouchPad Restart

[Service]
User=root
Type=oneshot
ExecStart="rmmod i2c_hid && modprobe i2c_hid"

[Install]
WantedBy=multi-user.target

```
Once this file is saved, all you need to do is start and enable the service.

```# systemctl start touchpadrestart```

```# systemctl enable touchpadrestart```


That's it! Quick and easy fix. (For touchpads other than this one, you can find the device driver name using ```lspci``` and change it in the script. )
