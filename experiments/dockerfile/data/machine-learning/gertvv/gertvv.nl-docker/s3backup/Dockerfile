FROM ruby:2.7-buster

WORKDIR /usr/src/app

COPY Gemfile Gemfile.lock ./
RUN  bundle config set --local path ./vendor/bundle
RUN  bundle install
COPY s3backup.sh rsa_key s3put.rb ./

CMD [ "./s3backup.sh" ]
