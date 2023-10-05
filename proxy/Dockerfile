# Use the jwilder/nginx-proxy image as the base
FROM jwilder/nginx-proxy

# Set a default value for CLIENT_MAX_BODY_SIZE if the environment variable is not provided
ENV MAX_BODY_SIZE="${CLIENT_MAX_BODY_SIZE:-128m}"

# Create and populate the client_max_body_size.conf file with the environment variable value
RUN echo "client_max_body_size $MAX_BODY_SIZE;" > /etc/nginx/conf.d/client_max_body_size.conf