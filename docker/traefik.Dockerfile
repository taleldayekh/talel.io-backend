FROM traefik:v2.4.0

COPY ../traefik/traefik.toml /etc/traefik/traefik.toml
COPY ../traefik/traefik_dynamic.toml /etc/traefik/traefik_dynamic.toml

VOLUME /etc/traefik/

# Share the directory in which certificates are stored
VOLUME /etc/letsencrypt/

# Share the Docker socket for Traefik to listen on for
# any container changes.
VOLUME /var/run/docker.sock
