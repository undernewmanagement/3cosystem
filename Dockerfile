FROM 3cosystem/website-onbuild:1.0.0

# Pass the command line arg into the ENV arg, persisting it in the docker image
ARG SITE_VERSION
ENV SITE_VERSION ${SITE_VERSION}
