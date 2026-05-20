FROM node:18-bullseye

WORKDIR /app

# Copy package configurations
COPY package.json package-lock.json ./
RUN npm ci

# Copy the rest of the application
COPY . .

# Set environment variable to make Jest exit properly
ENV CI=true

# Keep container running
CMD ["tail", "-f", "/dev/null"]
