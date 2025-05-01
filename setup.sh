#!/usr/bin/env bash

apt-get update
apt-get -y install bash

# playwright dependencies
# apt-get -y install libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2 libxkbcommon0 libatspi2.0-0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libpango-1.0-0 libcairo2 libx11-xcb1 libxcursor1 libgtk-3-0 libpangocairo-1.0-0 libcairo-gobject2 libgdk-pixbuf-2.0-0

curl -sL https://deb.nodesource.com/setup_lts.x | bash -
apt install -y nodejs
apt install -y npm
npm install npm@latest -g

# to run local server
npm install -g serve