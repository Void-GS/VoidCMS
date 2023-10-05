FROM node:lts-alpine3.18

ADD . /frontend/

ADD ./docker/.env-deploy /frontend/.env

RUN ls /frontend

WORKDIR /frontend

# RUN chmod +x /frontend/docker/init.sh

RUN yarn

RUN yarn build

# RUN rm -rf /frontend/node_modules

CMD [ "node", "/frontend/.output/server/index.mjs" ]



