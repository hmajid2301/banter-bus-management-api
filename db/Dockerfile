FROM mongo:4.4.4

ENV MONGO_INITDB_ROOT_USERNAME=banterbus \
	MONGO_INITDB_ROOT_PASSWORD=banterbus \
	MONGO_INITDB_DATABASE=banterbus

COPY db/data /data
COPY db/init.sh /
RUN chmod +x init.sh

CMD ["/init.sh"]