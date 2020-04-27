
FROM higbee/python36_base:latest
LABEL maintainer="Higbee_"

# Airflow
ARG AIRFLOW_VERSION=1.10.9
ARG AIRFLOW_USER_HOME=/usr/local/airflow
ARG AIRFLOW_DEPS=""
ARG PYTHON_DEPS=""
ENV AIRFLOW_HOME=${AIRFLOW_USER_HOME}

RUN set -ex \
    && apt-get update -yqq \
    && apt-get upgrade -yqq \
    && apt-get install -yqq --no-install-recommends \
    && apt-get install nano \
    && useradd -ms /bin/bash -d ${AIRFLOW_USER_HOME} airflow

# Copy config files and dags
COPY scripts/entrypoint.sh /entrypoint.sh
COPY config/airflow.cfg ${AIRFLOW_USER_HOME}/airflow.cfg
COPY . ${AIRFLOW_USER_HOME}/

RUN chown -R airflow: ${AIRFLOW_USER_HOME}

EXPOSE 8080 5555 8793

USER airflow
WORKDIR ${AIRFLOW_USER_HOME}
RUN pipenv install --deploy
ENTRYPOINT ["./scripts/entrypoint.sh"]
CMD ["webserver"]
