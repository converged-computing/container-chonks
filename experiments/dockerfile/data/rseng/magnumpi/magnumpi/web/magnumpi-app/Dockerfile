FROM emscripten/emsdk AS wasmbuilder

COPY src /src/src
COPY magnumpi /src/magnumpi
COPY external /src/external
COPY plutil /src/plutil
COPY web/assembly /src/web/assembly

RUN cd web/assembly && npm install -g npm@7 && npm install

RUN cd web/assembly && npm run build

FROM node:14 AS webpacker

COPY web/magnumpi-app /web/magnumpi-app
COPY web/assembly /web/assembly
COPY web/package.json /web/package.json
COPY web/package-lock.json /web/package-lock.json
COPY --from=wasmbuilder /src/web/assembly /web/assembly/dist
COPY ideas/lxcat/He_He+/schema/v1.1/interaction-potential.json /ideas/lxcat/He_He+/schema/v1.1/interaction-potential.json

RUN cd /web && npm install -g npm@7 && npm install
RUN cd /web/magnumpi-app && npm run build

FROM node:14

COPY --from=webpacker /web/magnumpi-app/dist /app

RUN npm install -g serve

EXPOSE 5000

CMD serve -l 5000 -s /app
