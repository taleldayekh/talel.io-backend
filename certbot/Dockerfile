FROM certbot/certbot:latest

VOLUME ["/var/www/html", "/etc/letsencrypt", "/var/lib/letsencrypt"]

CMD ["certonly", "--webroot", "-w", "/var/www/html", "--register-unsafely-without-email", "--agree-tos", "--staging", "-d", "www.talel.io", "-d", "talel.io"]
