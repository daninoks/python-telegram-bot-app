# python-telegram-bot-app


## Secure Nginx with Let's Encrypt
### Step 1: Install Certbot
Certbot is an open-source software tool for automatically enabling HTTPS using Let’s Encrypt certificates.

The first step to securing Nginx with Let’s Encrypt is to install Certbot:
```
sudo apt update
sudo apt install certbot python3-certbot-nginx
```
### Step 2: Check Nginx Configuration
As noted in the prerequisites, you should already have a registered domain and an Nginx server block for that domain. As an example, this article uses the domain example.com.
To check whether it is set up correctly, open the Nginx configuration file:
```
sudo nano /etc/nginx/sites-available/example.com
```
Then, locate the server_name directive and make sure it is set to your domain name. As you want to include the domain name with and without the www. prefix, the line should look similar to the one below:
```
server_name example.com www.example.com;
```
>Note: If you need to make changes to the Nginx configuration file, make sure to save the modified file. Then, check the configuration syntax with the command **sudo nginx -t** and restart the service with **sudo systemctl reload nginx**
