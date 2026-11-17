# Define PHP version as build argument with default value
ARG PHP_VERSION="8.1"

# Use the specified PHP version to create the image
FROM php:${PHP_VERSION}-apache

LABEL maintainer="Melih Cetinkaya"
LABEL description="PHP application with Apache web server"
LABEL version="1.0"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libzip-dev \
    libpq-dev \
    zip \
    unzip \
    && docker-php-ext-install zip pdo pdo_mysql pdo_pgsql \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy PHP file
COPY index.php /var/www/html/

# Set proper permissions
RUN chown -R www-data:www-data /var/www/html \
    && chmod -R 755 /var/www/html

# Expose port 80
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost/ || exit 1