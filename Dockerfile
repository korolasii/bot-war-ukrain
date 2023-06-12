# FROM python:3.9

# RUN mkdir -p /docker/app/bot-war-info/
# WORKDIR /docker/app/bot-war-info/

# COPY . /docker/app/bot-war-info/
# RUN pip install -r req.txt

# CMD ["python","main.py"]

FROM python:3.9

# Установка Chrome
RUN apt-get update && apt-get install -y \
    xvfb \
    xauth \
    xfonts-base \
    wkhtmltopdf \
    libfontconfig1 \
    libxrender1 \
    && apt-get clean

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y google-chrome-stable \
    && apt-get clean

RUN mkdir -p /docker/app/bot-war-info/
WORKDIR /docker/app/bot-war-info/

COPY . /docker/app/bot-war-info/
RUN pip install -r req.txt


VOLUME /docker/app/bot-war-info/picture

CMD ["python", "-u","main.py"]
