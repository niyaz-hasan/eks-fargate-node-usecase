# Stage 1: Build the React application
FROM node:16-alpine as build

WORKDIR /app

# Copy package files first for better caching
COPY package.json  ./

# Install dependencies
RUN npm install 

# Copy all source files
COPY . .

# Build the application
RUN npm run build

# Stage 2: Serve the application using Nginx
FROM nginx:1.21-alpine

# Copy built assets from the previous stage
COPY --from=build /app/build /usr/share/nginx/html

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]