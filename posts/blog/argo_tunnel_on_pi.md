title="Setting up Cloudflare Argo Tunnel on Raspberry Pi"
description="Quick tutorial for setting up argo tunnel to host your website locally from your Raspberry Pi"
date="2021-12-08"
+++
This is a way to set up cloudflare argo tunnel on your Raspberry Pi to host your own webserver without port forwarding.

##### KEEP IN MIND THAT THIS IS NOT RECOMMENDED FOR SENSITIVE DATA AS IT WILL BE PASSING THROUGH CLOUDFLARE SERVERS.

#### What is argo tunnel?

It is a tunneling service provided by Cloudflare to help users tunnel connections to their servers via the cloudflare network. It has multiple use cases but here we will only use it for one thing: 

#### Why argo tunnel?

It is used to tunnel your webserver to the internet. Usually if you want your web app hosted on your PC to be accessible by the world, you need to have your ports open for incoming requests. If your ISP is restrictive like mine, they give you an in-network IP that is not accessible from anywhere else, so your regular port forwarding settings won't work. Think of it like your router is itself connected to a bigger router.

#### Requirements

1. A [cloudflare](https://dash.cloudflare.com/sign-up/) account.
2. A domain name, it's nameservers pointing to cloudflare (preferably the whole domain managed by cloudflare).
3. A Raspberry Pi
4. A webpage/site/server that you want to open to the world.

#### How to set up one?

1. Download the latest binary of `cloudflared` tool for your device. 
***Note: for the raspberry pi, the newer versions have trouble installing. I personally use an older version which is available at the following link.***

`wget https://bin.equinox.io/c/VdrWdbjqyF/cloudflared-stable-linux-arm.tgz`

2. put the binary in your PATH so that it can be called upon.

3. use the `cloudflared` binary to log in to your cloudflared account. 

4. type `cloudflared login`, and it will give you a link.
4. Copy that link and open it in your browser to authorise the log in.
4. Create a test tunnel by following this syntax:
		`cloudflared --hostname yourdomain.xyz --url http://localhost`
5. Once this is done, you can copy the cert file that is created `### cp ~/.cloudflared/cert.pem /etc/cloudflared`
3. use your editor to create `/etc/cloudflared/config.yml`
5. You can fill it like this:
   	```
	hostname: your_domain.xyz
	url: http://localhost

6. Install the cloudflared service

	`### cloudflared service install --legacy` 
(Make sure the legacy flag is active because we are using an older version of cloudflared)

Hope this tutorial helped you. Now your local webserver will be accessible from your domain!

#### Done
