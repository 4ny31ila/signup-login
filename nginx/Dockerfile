# Use the official Nginx image.
FROM nginx:latest

# Remove the default Nginx configuration file.
RUN rm /etc/nginx/conf.d/default.conf

# Copy the custom Nginx configuration file.
COPY nginx.conf /etc/nginx/nginx.conf
