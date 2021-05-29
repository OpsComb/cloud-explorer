###########
# BUILDER #
###########

ARG APP_HOME=/usr/local/src/cloud_explorer

FROM openresty/openresty:1.19.3.1-alpine as base
RUN apk add py3-pip

# pull official base image
FROM base as builder

ARG APP_HOME

# set work directory
WORKDIR $APP_HOME

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add gcc musl-dev build-base python3-dev


COPY Pipfile Pipfile.lock ./

RUN pip3 install --upgrade pip setuptools \
           && pip3 install pipenv wheel \
           && pipenv lock -r > requirements.txt \
           && pip3 wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

###############
# DEBUG BUILD #
###############
FROM base as debug

ARG APP_HOME

RUN apk add curl bash vim procps

COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder $APP_HOME/requirements.txt .
RUN pip install --no-cache /wheels/* --ignore-installed six

# copy project
COPY . $APP_HOME

WORKDIR $APP_HOME

# executing entrypoint is not required in debug builds

CMD ["python manage.py runserver 0.0.0.0:8000"]


##############
# PROD BUILD #
##############

# pull official base image
FROM base as prod

ARG APP_HOME

# install dependencies
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder $APP_HOME/requirements.txt .

RUN pip3 install --no-cache /wheels/* --ignore-installed six && rm -rf /wheels/

WORKDIR $APP_HOME

# copy entrypoint.sh
ADD entrypoint.sh /usr/local/bin/

RUN chmod +x /usr/local/bin/entrypoint.sh

# copy project
COPY cloud_explorer/ ./

# run entrypoint.sh
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

CMD ["/usr/bin/supervisord"]
