sudo DEBIAN_FRONTEND=noninteractive apt-get install -y python3-pip python3-venv && \
  pip3 install beautifulsoup4 

pip3 install --user requests

python3 -m venv venv && source venv/bin/activate && pip install beautifulsoup4 && python3 novo.py