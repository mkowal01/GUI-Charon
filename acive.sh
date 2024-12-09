#!bin/bash
sudo apt update
sudo apt install python python3-venv python3-pip -y
mkdir inzynier
cd inzynier
python3 -m venv venv_kivy

sudo apt update
sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv build-essential git
sudo apt install -y \
    python3-dev \
    libgles2-mesa-dev \
    libegl1-mesa-dev \
    libgbm-dev \
    libx11-dev \
    libmtdev-dev \
    libxcursor-dev \
    libxi-dev \
    libxrandr-dev \
    libxinerama-dev \
    libxxf86vm-dev \
    libsqlite3-dev \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    pkg-config
sudo apt install -y gstreamer1.0-plugins-base gstreamer1.0-plugins-good
