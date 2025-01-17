#!/bin/bash
# Zainstaluj niezb�dne pakiety do budowy Pythona
sudo apt update
sudo apt install -y wget build-essential zlib1g-dev libssl-dev libncurses5-dev libncursesw5-dev libreadline-dev \
libsqlite3-dev libgdbm-dev libdb5.3-dev libbz2-dev libexpat1-dev liblzma-dev tk-dev

# Pobierz �r�d�a Pythona 3.10.0
wget https://www.python.org/ftp/python/3.10.0/Python-3.10.0.tgz

# Rozpakuj �r�d�a
tar -xvf Python-3.10.0.tgz

# Przejd� do katalogu �r�d�owego
cd Python-3.10.0

# Skonfiguruj i zbuduj Pythona
./configure --enable-optimizations
make -j $(nproc)

# Zainstaluj now� wersj� Pythona
sudo make altinstall
