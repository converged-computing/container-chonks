####################################################################
### The base PHP and Nginx images for development and production ###
####################################################################

# Build argument: Build environment (dev, prod, test)
ARG BUILD_ENV=dev

# Build argument: Image tag
ARG IMAGE_TAG=8.1-fpm-buster

# Build argument: Folder with image files
ARG IMAGE_FILES_FOLDER

###############################
### Stage: Base Nginx image ###
###############################
FROM nginx:1.17.9 as nginx-dev

# Installs curl
# RUN apt-get update && apt-get install curl -y

# Copies scripts and configs
COPY nginx/image-files/ /

# Sets permissions for scripts
RUN chmod +x /docker-entrypoint.sh

# Changes entrypoint
ENTRYPOINT ["/docker-entrypoint.sh"]

# Starts Nginx
CMD ["nginx", "-g", "daemon off;"]


#############################
### Stage: Base PHP image ###
#############################
FROM php:$IMAGE_TAG as php-dev

# Installs libraries
RUN apt-get update && apt-get install -y \
    git \
    zip \
    unzip \
    zlib1g-dev \
    libzip-dev \
    libfreetype6-dev \
    libjpeg-dev \
    libwebp-dev \
    libpng-dev \
    libicu-dev

# Installs PHP extensions
RUN docker-php-ext-configure gd --with-freetype=/usr/include/ --with-jpeg=/usr/include/ --with-webp=/usr/include/ \
    && docker-php-ext-install \
    bcmath \
    intl \
#    mcrypt \
    pdo_mysql \
    gd \
    zip \
    opcache

# Sets PATHs
ENV PATH=/app:/app/vendor/bin:/root/.composer/vendor/bin:$PATH

# Installs Composer
ENV COMPOSER_ALLOW_SUPERUSER=1
ARG COMPOSER_VERSION=2.3.10
RUN curl -sS https://getcomposer.org/installer | php -- \
        --filename=composer \
        --install-dir=/usr/local/bin \
        --version=${COMPOSER_VERSION} \
    && composer clear-cache

# Prepares for loading private Composer dependencies
RUN mkdir -p ~/.ssh && ssh-keyscan -H gitlab.com >> ~/.ssh/known_hosts

# Expands the rights for www-data user
RUN usermod -u 1000 www-data

# Sets the working directory
WORKDIR /app

# Sets up XDebug
ARG XDEBUG_ENABLED=false
RUN if $XDEBUG_ENABLED; then pecl install xdebug \
    && docker-php-ext-enable xdebug \
    && echo "xdebug.mode=debug" >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini \
    && echo "xdebug.max_nesting_level=1000" >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini \
    ; fi

# Copies base scripts and configs
COPY base/image-files/ /

# Build argument: Folder with image files
ARG IMAGE_FILES_FOLDER

# Copies custom scripts and configs
COPY $IMAGE_FILES_FOLDER/image-files/ /

# Build argument: Debug mode — enables debug info display (it should be disabled on production!)
ARG DEBUG_MODE=1

# Enables or disables PHP error reporting depending on `DEBUG_MODE`
RUN if [ "$DEBUG_MODE" = 0 ]; then sed -i '/display_errors = On/cdisplay_errors = Off' /usr/local/etc/php/conf.d/base-custom.ini; fi

# Sets permissions for scripts
RUN chmod +x /build-scripts/build
RUN chmod +x /usr/local/bin/*

# Build argument: Build environment (dev, prod, test)
ARG BUILD_ENV

# Application environment for both Symfony 3.x and 4.x
ENV APP_ENV=$BUILD_ENV`

# Build argument: Built-in variable for app version
ARG APP_VERSION="1111111111111111111111111111111111111111 Thu Mar 20 00:00:00 2020 +0000"
# Build argument: Built-in variable for active git branch name
ARG BRANCH=no-branch

# Application version (built in the image)
#ENV AE_APP_VERSION=$APP_VERSION
# Active git branch name (built in the image)
#ENV AE_ACTIVE_BRANCH=$BRANCH

# Builds the source code for production environment (optional)
RUN /build-scripts/build

# Starts the app
CMD ["app-bootstrap"]

################################################################################
### Stage: Interim builder image for Composer dependencies and cache warm-up ###
################################################################################
FROM php-dev as builder-composer

# Copies SSH key
COPY base/ssh/id_rsa /root/.ssh/id_rsa

# Prepares SSH key
RUN chmod 0600 /root/.ssh/id_rsa

# Build argument: Folder with image files
ARG IMAGE_FILES_FOLDER

# Copies Composer files
COPY $IMAGE_FILES_FOLDER/app/composer.* /app/

# Loads vendors and prepares binaries (this should be cached if Composer files have not been changed)
RUN composer install --no-dev --no-scripts

# Creating missing cache folders
RUN mkdir -p var/cache

# Copies all files
COPY $IMAGE_FILES_FOLDER/app /app

# Runs Composer related scripts and optimizes the autoloader
RUN composer install --no-dev --classmap-authoritative

##########################################################
### Stage: Interim builder image for Yarn dependencies ###
##########################################################
FROM node:16.13-alpine as builder-yarn

# Sets the working directory
WORKDIR /app

# Installs Git
RUN apk --update add git less openssh && \
    rm -rf /var/lib/apt/lists/* && \
    rm /var/cache/apk/*

# Build argument: Folder with image files
ARG IMAGE_FILES_FOLDER

# Copies frontend-related files
COPY $IMAGE_FILES_FOLDER/app/package.json /app/
COPY $IMAGE_FILES_FOLDER/app/yarn.lock /app/

# Installs Yarn dependencies
RUN yarn install

##############################################################
### Stage: Interim builder image for building the frontend ###
##############################################################
FROM builder-yarn as builder-frontend

# Build argument: Folder with image files
ARG IMAGE_FILES_FOLDER

# Copies frontend source
COPY $IMAGE_FILES_FOLDER/app/frontend /app/frontend

# Copies vendor assets
#COPY --from=builder-composer /app/vendor/sylius/ui-bundle/Resources/private \
#    /app/vendor/sylius/ui-bundle/Resources/private

# Build argument: Build environment (dev, prod, test)
ARG BUILD_ENV

# Warms up the cache
RUN yarn run build:$BUILD_ENV
