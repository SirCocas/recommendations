sudo DEBIAN_FRONTEND=noninteractive apt-get install -y python3-pip python3-venv && \
  pip3 install beautifulsoup4 

curl https://www.anime-planet.com/anime/chainsaw-man-the-movie-reze-arc/recommendations

python3 -m venv venv && source venv/bin/activate && pip install beautifulsoup4 && pip install requests && python3 novo.py