FROM python:3.10

ENV PROJECT markodon
WORKDIR /opt/${PROJECT}

RUN apt-get update -y && \
    apt-get install -y jq make

COPY ./ /opt/${PROJECT}
RUN python -m pip install -r requirements.txt

COPY docker-config/bashrc /root/.bashrc
COPY ./docker-config/entrypoint.sh /usr/local/bin/entrypoint
RUN chmod +x /usr/local/bin/entrypoint
ENTRYPOINT ["/usr/local/bin/entrypoint"]
