FROM ruby:3.1.2-buster

ENV SITE_DIR=/var/jekyll

RUN echo "gem: --no-ri --no-rdoc" > ~/.gemrc

RUN yes | gem update --system
RUN gem install --force bundler

# copy just the gemfile so other file changes
# do not bust the bundle install cache
RUN mkdir -p $SITE_DIR
COPY Gemfile* $SITE_DIR
WORKDIR $SITE_DIR
RUN bundle install

COPY . $SITE_DIR

CMD ["jekyll", "serve", "-H", "0.0.0.0", "-P", "4000", "--force_polling", "--livereload", "-s", "./docs"]
ENTRYPOINT ["./entrypoint"]

EXPOSE 4000


