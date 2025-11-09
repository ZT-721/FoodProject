# Stage 1: Build the React app
FROM node:18-alpine AS build
WORKDIR /app

# Copy package.json and install dependencies
# We copy only package.json first to leverage Docker layer caching
COPY frontend/package*.json ./
RUN npm install

# Copy the rest of the frontend code
COPY frontend/ ./

# Build the static files. This will use .env file for build-time variables.
RUN npm run build

# Stage 2: Serve the static files with a production-ready server
FROM node:18-alpine
WORKDIR /app

# Install `serve` to act as the static file server
RUN npm install -g serve

# Copy the built static files from the build stage
COPY --from=build /app/build ./build

# Expose the port `serve` will run on
EXPOSE 3000

# The command to start the server. 
# -s flag means it's a single-page app.
# -l flag specifies the listener port.
CMD ["serve", "-s", "build", "-l", "3000"]
