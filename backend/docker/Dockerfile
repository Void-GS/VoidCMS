FROM python:3.11-alpine3.18


ADD . /backend/

ADD ./docker/settings-deploy.py /backend/backend/settings.py

WORKDIR /backend

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

RUN chmod +x /backend/docker/init.sh

CMD [ "/bin/sh", "/backend/docker/init.sh" ]
