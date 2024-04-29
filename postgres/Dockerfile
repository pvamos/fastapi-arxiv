# Use the official PostgreSQL Alpine image
FROM postgres:16.2-alpine3.19

# Install locale support
RUN apk add --no-cache --update musl-locales musl-locales-lang

# Set the default locale to one that is available in the package
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

#WORKDIR /code
#COPY ./wait-for.sh /code/wait-for.sh
#RUN chmod +x /code/wait-for.sh
