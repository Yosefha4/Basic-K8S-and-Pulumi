# Use the official Nginx image as the base image
FROM nginx:alpine

# Copy the index.html file into the container
COPY src/html /usr/share/nginx/html

# Expose port 80 (Nginx's default HTTP port)
EXPOSE 80

# Start Nginx when the container starts
CMD ["nginx", "-g", "daemon off;"]

