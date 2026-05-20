FROM node:18-bullseye

WORKDIR /app

# Copy package configurations
COPY package.json package-lock.json ./
RUN npm ci

# Copy only the necessary application source files explicitly to avoid adding tests/ and solution/ to the image
COPY src/ ./src/
COPY public/ ./public/
COPY .firebaserc firebase.json firestore.rules storage.rules firestore.indexes.json ./

# Set environment variable to make Jest exit properly
ENV CI=true

# Keep container running
CMD ["tail", "-f", "/dev/null"]
