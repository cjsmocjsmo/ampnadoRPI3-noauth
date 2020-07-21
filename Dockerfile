FROM amp-build-deps:latest

RUN mkdir /usr/share/Ampnado
COPY ampnado /usr/share/Ampnado
WORKDIR /usr/share/Ampnado
RUN \
	chmod -R 0755 /usr/share/Ampnado && \
	chown -R root:root /usr/share/Ampnado

CMD [ "python3", "/usr/share/Ampnado/ampnado.py" ]