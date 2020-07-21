FROM amp-build-deps:latest

RUN \
	mkdir /usr/share/Ampnado && \
	chmod -R 0755 /usr/share/Ampnado

COPY ampnado /usr/share/Ampnado

RUN \
	chmod -R 0755 /usr/share/Ampnado/static && \
	chmod -R 0755 /usr/share/Ampnado/static/images && \
	chmod -R 0755 /usr/share/Ampnado/static/images/thumbnails

CMD [ "python3", "/usr/share/Ampnado/ampnado.py" ]