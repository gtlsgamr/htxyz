title=Setting up a basic mail server
description=How to set up a basic mail server using postfix + dovecot.
date=2022-11-04
+++
After messing around for a LONG time, I finally have a way to set up a basic
mail server using postfix + dovecot.

### What this post will help you get

- A mail server on your linux system with which you can send standard encrypted e-mails.
- Ability to connect with the given mail server via your own mail client
- Mailboxes for all the users of the system in their homedir. ~/.Mail
- Authentication using the linux system login

## What you won't get
- DKIM, Spam prevention etc. (Maybe I will update it later when I feel like) **NOTE:** As I painfully found out later, DKIM - SPF - DMARC records are a must otherwise google and microsoft will auto reject your emails. I will add them here when I get time.
- A guarantee that big players like google and microsoft **will not blacklist
  or spam filter your emails**.

## What you will need
- A linux server with port 25 allowed
- Ubuntu / Debian (You are free to use your distro of choice but YMMW)
- Certbot

## The steps

Install postfix and dovecot.


sudo apt-get install postfix dovecot-common dovecot-imapd dovecot-pop3d

	

Open the postfix config file at /etc/postfix/main.cf and clear it. Replace
the contents with the below code, but make sure you change some variables
accordingly.

    smtpd_banner = $myhostname ESMTP $mail_name (Debian/GNU)
    biff = no
    append_dot_mydomain = no
    readme_directory = no
    compatibility_level = 2
    smtpd_tls_cert_file=/etc/letsencrypt/live/example.com/fullchain.pem
    smtpd_tls_key_file=/etc/letsencrypt/live/example.com/privkey.pem
    smtpd_tls_security_level=may
    smtp_tls_security_level=may
    smtp_tls_session_cache_database = btree:${data_directory}/smtp_scache
    smtpd_relay_restrictions = permit_mynetworks permit_sasl_authenticated
    defer_unauth_destination
    myhostname = example.com
    alias_maps = hash:/etc/aliases
    alias_database = hash:/etc/aliases
    myorigin = /etc/mailname
    mydestination = $myhostname, example.com, localhost.in, , localhost
    relayhost =
    mynetworks = 127.0.0.0/8 [::ffff:127.0.0.0]/104 [::1]/128
    mailbox_size_limit = 0
    recipient_delimiter = +
    inet_interfaces = all
    inet_protocols = ipv4
    home_mailbox = .Mail/
    smtpd_sasl_type = dovecot
    smtpd_sasl_path = private/auth

For line number 6 and 7 in the above code you will have to generate
   certificates using certbot for whichever domain you want to use.
	

sudo certbot -d example.com


Open /etc/postfix/master.cf and uncomment the line that starts with submission.

submission inet n - y - - smtpd

Now moving on to dovecot configuration, the default is fine apart from some minor changes listed below.

For /etc/dovecot/dovecot.conf,
add the below lines:

    protocols = imap pop3
    listen = *, ;;

In /etc/dovecot/conf.d/10-ssl.conf define the path for the certificates you created before.

In /etc/dovecot/conf.d/10-mail.conf, edit the following

mail_location = maildir:~/.Mail

Restart postfix and dovecot.

    sudo systemctl restart postfix.service
    sudo systemctl restart dovecot.service

I will not post testing and such, this is supposed to be a reference guide not a tutorial. Have fun!
