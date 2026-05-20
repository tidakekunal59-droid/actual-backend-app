FROM node:18

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./
COPY function/package*.json ./function/

# Install dependencies globally or locally as needed
RUN npm install
RUN cd function && npm install

# Copy all project files
COPY . .

# Keep container running for agent
CMD ["tail", "-f", "/dev/null"]
