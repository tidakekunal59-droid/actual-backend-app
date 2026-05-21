FROM node:18-bullseye
WORKDIR /app
RUN apt-get update \
    && apt-get install -y --no-install-recommends python3 python3-pytest \
    && rm -rf /var/lib/apt/lists/*
COPY package.json ./
COPY src ./src
ENV CI=true
CMD ["tail", "-f", "/dev/null"]
