# Use the syslog-nd Alpine image from https://hub.docker.com/r/linuxserver/syslog-ng
FROM linuxserver/syslog-ng:4.5.0

# Install locale support
#RUN apk add --no-cache --update musl-locales musl-locales-lang

# Set the default locale to one that is available in the package
#ENV LANG en_US.UTF-8
#ENV LANGUAGE en_US:en
#ENV LC_ALL en_US.UTF-8

ENV PUID 1000
ENV PGID 1000
ENV TZ Etc/UTC

