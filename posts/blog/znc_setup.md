title="Setting up znc with a subdomain using NGINX"
description="Quick tutorial on setting up ZNC - IRC bouncer with an nginx reverse proxy"
date="2022-16-09"
+++
This post covers ubuntu/debian and systemd based operating systems. Although
minor differences may exist, similar principle can be applied to other systems
as well. Setting up znc on a linux machine is easy, and setting it up with a
subdomain is easy as well! We will be using a standard znc installation and use
certbot to generate SSL certificates.

### Requirements
- [znc](https://wiki.znc.in/Installation)
- [nginx](https://nginx.org/en/)
- [certbot](https://certbot.eff.org/)

### Installation

Install znc using any method explained on the [main site](https://wiki.znc.in/Installation). 

If you are on ubuntu, you can install znc and nginx using 

`sudo apt install znc nginx certbot`

### Configuration

Once that is done, we need to create config file for znc. That can be done by 

`znc --makeconf`

It will ask you multiple questions, here is how I answered them:

	   Listen on port: 1025    
	   Listen using SSL: yes    
	   Listen using both IPv4 and IPv6: no    
	   Username: your_username    
	   Enter password: your_password     
	   Confirm password: your_password            
	   Nick: nick     
	   Alternate nick: nick_    
	   Real name: optional    
	   Bind host:    
	   Set up a network? no    
	   Launch ZNC now? no    

At this point znc has created your config file at

`$HOME/.znc/configs/znc.conf`. 
Now we modify the config so that there are two listeners instead of one. **(Note how
one allows web interface while the other is for IRC, both on different
ports.)** You will use the first one to modify znc settings and the second one
to access znc network via IRC.

	<Listener listener0>
		AllowIRC = false
		AllowWeb = true
		IPv4 = true
		IPv6 = false
		Port = 31337
		SSL = true
		URIPrefix = /
	</Listener>

	<Listener listener1>
		AllowIRC = true
		AllowWeb = false
		IPv4 = true
		IPv6 = false
		Port = 1337
		SSL = true
		URIPrefix = /
	</Listener>

You can start znc by simply entering `znc`.

### Setting up reverse proxy

All that is left now is to configure nginx so that it will pass the
subdomain requests to znc. Create the znc config file at
`/etc/nginx/sites-enabled/znc` **Make sure your DNS record for selected subdomain point to the IP of your host.**

	server {
		server_name znc.yourdomain.xyz;
		access_log  /var/log/nginx/znc-access.log;
		error_log   /var/log/nginx/znc-error.log;

		location / {
			proxy_pass https://127.0.0.1:31337/;
		}
	}

After this check for errors in the configuration:
`sudo nginx -t`

Restart nginx service from systemd:
`sudo systemctl restart nginx`

One last thing left to do is generate ssl certificates for the znc subdomain.
You can do that by using `certbot` command. Enter it and follow the
instructions to proceed.

Now your znc web interface should be accessible from `znc.yourdomain.xyz`
