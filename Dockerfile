FROM alpine:3.13

ENV PYTHONUNBUFFERED True

ENV APP_HOME /app

ENV USER web-user

RUN addgroup -S $USER && adduser -S $USER -G $USER

WORKDIR $APP_HOME

COPY --chown=$USER requirements.txt $APP_HOME/

RUN apk add --no-cache \
            python3 py3-pip py3-wheel gettext mailcap \
            uwsgi uwsgi-python3 uwsgi-http \
            py3-psycopg2 \
    && pip install -r requirements.txt \
    && rm -rf /root/.cache/ \
    && chown -R $USER:$USER $APP_HOME

COPY --chown=$USER . $APP_HOME/

USER $USER

RUN python3 manage.py compilemessages \
    && python3 manage.py collectstatic --noinput

RUN coverage run manage.py test --verbosity 2 \
    && coverage report -m --fail-under=100 \
    && coverage erase

EXPOSE 8000

CMD exec uwsgi --ini uwsgi.ini
