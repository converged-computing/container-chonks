FROM mongrelion/ruby:2.2.2

MAINTAINER Carlos León <mail@carlosleon.info>

ENV RAILS_ENV production

EXPOSE 3000

WORKDIR /usr/src/app

RUN apt-get update && \
    apt-get -y install nodejs && \
    git clone git://github.com/fulcrum-agile/fulcrum.git . && \
    sed -i "s/2.2.1/2.2.2/" Gemfile && \
    bundle install --deployment --without development test postgres mysql && \
    bundle exec rake fulcrum:setup db:setup assets:precompile && \

ENTRYPOINT ["bundle", "exec", "rails", "s"]
