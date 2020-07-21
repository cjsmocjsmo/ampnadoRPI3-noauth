FROM debian:buster-slim

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
	pip3 install pymongo==3.4.0 tornado==3.2.1 mutagen==1.43.0

CMD [ "/bin/sh" ]