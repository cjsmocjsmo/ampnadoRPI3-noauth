FROM debian:bullseye-slim
RUN mkdir /usr/share/Ampnado
COPY ampnado /usr/share/Ampnado
WORKDIR /usr/share/Ampnado
RUN \
	chmod -R 0755 /usr/share/Ampnado && \
	chown -R root:root /usr/share/Ampnado
RUN \
	apt-get update && \
	apt-get dist-upgrade -y && \
	apt-get autoclean -y && \
	apt-get autoremove -y && \
	apt-get install --no-install-recommends -y \
		zlib1g-dev \
		libjpeg-dev \
		python3-dev \
        python3-setuptools \
        python3-wheel \
		python3-pil \
		python3-pip
RUN \
	python3.8 -m pip install --upgrade pip setuptools wheel && \
	pip3 install pymongo==3.4.0 tornado==3.2.1 mutagen==1.43.0

CMD [ "python3", "/usr/share/Ampnado/ampnado.py" ]