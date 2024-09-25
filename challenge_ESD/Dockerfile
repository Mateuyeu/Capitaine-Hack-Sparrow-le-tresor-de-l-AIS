# Utiliser une image de base Ubuntu
FROM ubuntu:20.04

# Définir le fuseau horaire non interactif
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Paris

# Installer les dépendances nécessaires
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    git \
    wget \
    libssl-dev \
    libffi-dev \
    build-essential \
    tzdata \
    knockd \
    iptables \
    opencpn \
    # pour réduire la taille de l'image
    && rm -rf /var/lib/apt/lists/* 

# Cloner et installer AISdecoder
RUN git clone https://github.com/schwehr/libais.git /opt/libais && \
    cd /opt/libais && \
    python3 setup.py install && \
    # Supprimer le répertoire source après l'installation
    rm -rf /opt/libais  

# Installation de Flask
RUN pip3 install flask requests
RUN apt-get update && apt-get install -y sudo
RUN echo "root ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

# Copier les fichiers pour le challenge
COPY scripts/default.txt /opt/default.txt
COPY scripts/gestion_login.js /opt/static/gestion_login.js
COPY scripts/simulate_ais.py /opt/simulate_ais.py
COPY scripts/app.py /opt/app.py
COPY scripts/ais_interface.html /opt/ais_interface.html

# Créer un utilisateur non-root "appuser"
RUN useradd -m appuser

# Exposer les ports utiliser par le serveur AIS
EXPOSE 12346/udp 80

RUN echo '#!/bin/bash' > /entrypoint.sh && \
    echo 'set -x' >> /entrypoint.sh && \
    echo 'python3 /opt/app.py & sleep 5 && python3 /opt/simulate_ais.py' >> /entrypoint.sh && \
    chmod +x /entrypoint.sh

# Changer les permissions des fichiers pour l'utilisateur non-root
RUN chown -R appuser:appuser /opt

USER appuser

ENTRYPOINT ["/entrypoint.sh"]
CMD ["sh", "-c", "python3 /opt/app.py & python3 /opt/simulate_ais.py & tail -f /dev/null"]