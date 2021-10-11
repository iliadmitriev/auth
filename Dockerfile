FROM alpine:3.14

ENV PYTHONUNBUFFERED True

ENV APP_HOME /app

ENV USER web-user

RUN addgroup -S $USER && adduser -S $USER -G $USER

WORKDIR $APP_HOME

COPY --chown=$USER requirements.txt $APP_HOME/

RUN apk add --no-cache \
                python3 \
                postgresql-libs icu-libs libpq \
                py3-pip \
                py3-wheel \
                gettext \
                mailcap \
    && apk add --no-cache --virtual .build-deps \
                build-base \
                python3-dev \
                postgresql-dev \
                linux-headers \
    && pip install --no-cache-dir --ignore-installed six -r requirements.txt \
    && apk del .build-deps \
    && rm -rf /root/.cache/ \
    && chown -R $USER:$USER $APP_HOME

COPY --chown=$USER . $APP_HOME/

USER $USER

RUN python3 manage.py compilemessages \
    && python3 manage.py collectstatic --noinput

EXPOSE 8000

STOPSIGNAL SIGINT

CMD exec uwsgi --ini uwsgi.ini
