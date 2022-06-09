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

### Step 3: Adjust Firewall to Allow HTTPS Traffic
The next step is to adjust the firewall to allow HTTPS traffic.
If you followed the Nginx installation guide, you already enabled your firewall to allow Nginx HTTP. As you are adding Let’s Encrypt certificates, you need to configure the firewall for encrypted traffic.

#### 1. To ensure your firewall is active and allows HTTPS traffic, run the command:
```
$ sudo ufw status | grep Nginx
Nginx HTTP                 ALLOW        Anywhere                  
Nginx HTTP (v6)            ALLOW        Anywhere (v6)             
```

>Nginx has three (3) profiles you can add as rules:
**Nginx HTTP (opens port 80)**
**Nginx HTTPS (opens port 443 – encrypted traffic)**
**Nginx Full (opens port 80 and 443)**

2. To allow encrypted traffic, you can either add the Nginx HTTPS profile or use Nginx Full and delete the existing Nginx HTTP rule:

##### Allow Nginx HTTPS traffic by running the command:
```
sudo ufw allow 'Nginx HTTPS'
```
##### Remove Nginx HTTP and use Nginx Full instead with:
```
sudo ufw deny 'Nginx HTTP'
```
```
sudo ufw allow 'Nginx Full'
```
3. Verify you added a rule that allows HTTPS traffic by using the **ufw status** command.
```
$ sudo ufw status | grep Nginx
Nginx HTTPS                ALLOW       Anywhere                  
Nginx HTTP                 DENY        Anywhere                  
Nginx Full                 ALLOW       Anywhere                  
Nginx HTTPS (v6)           ALLOW       Anywhere (v6)             
Nginx HTTP (v6)            DENY        Anywhere (v6)             
Nginx Full (v6)            ALLOW       Anywhere (v6)        
```
### Step 4: Obtain the SSL/TLS Certificate
Nginx’s plugin for Certbot reconfigures Nginx and reloads its configuration when needed. Therefore, the only thing you need to do is generate certificates with the NGINX plug‑in.

1. To do so, run the command:
```
sudo certbot --nginx -d example.com -d www.example.com
```
2. The output asks you to configure your HTTPS settings. Enter your email address and agree to the terms of service to continue.

3. Once you configure HTTPS, Certbot completes generating the certificate and reloads Nginx with the new settings.

4. Finally, the output displays that you have successfully generated a certificate and specifies the location of the certificate on your server.
### Step 5: Enable Automatic Certificate Renewal
Since Let’s Encrypt certificates expire every 90 days, Nginx recommends setting up and automatic renewal cron job.

1. First, open the crontab configuration file for the current user:
```
crontab -e
```
2. Add a cron job that runs the certbot command, which renews the certificate if it detects the certificate will expire within 30 days. Schedule it to run daily at a specified time (in this example, it does so at 05:00 a.m.):
```
0 5 * * * /usr/bin/certbot renew --quiet
```
The cron job should also include the --quiet attribute, as in the command above. This instructs certbot not to include any output after performing the task.
3. Once you added the cron job, save the changes, and exit the file.
