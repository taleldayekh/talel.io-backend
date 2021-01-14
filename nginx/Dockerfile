FROM nginx:latest

# Remove default configurations
# and add custom configurations.
RUN rm /etc/nginx/conf.d/default.conf
ADD nginx.conf /etc/nginx/conf.d/

VOLUME ["/etc/nginx/conf.d", "/var/www/html", "/etc/letsencrypt", "/var/lib/letsencrypt"]
