FROM php:8.3-fpm

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    libpng-dev \
    libonig-dev \
    libxml2-dev \
    libzip-dev \
    zip \
    unzip \
    libicu-dev

# Install PHP extensions
RUN docker-php-ext-install pdo_mysql mbstring exif pcntl bcmath gd zip intl

# Install Composer
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

# Install Redis extension
RUN pecl install redis && docker-php-ext-enable redis

# Install Meilisearch PHP SDK dependencies
RUN apt-get install -y pkg-config

# Set working directory
WORKDIR /var/www/html

# Create app user
RUN useradd -G www-data,root -u 1000 -d /home/appuser -s /bin/bash -m appuser

# Copy existing application directory permissions
RUN chown -R appuser:www-data /var/www/html

# Change to app user
USER appuser

# Expose port 9000 for PHP-FPM
EXPOSE 9000

CMD ["php-fpm"]

