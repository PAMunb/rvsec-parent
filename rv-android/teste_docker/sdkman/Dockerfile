FROM python:3.10-slim-bullseye

ENV DEBIAN_FRONTEND=noninteractive

SHELL ["/bin/bash", "-c"]

RUN apt-get update && \
    apt install -qq -y --no-install-recommends curl wget zip unzip git nano software-properties-common && \
    apt autoremove -y && \
    apt clean all && \
	rm -rf /var/lib/apt/lists/* && \
	rm -rf /tmp/*

RUN curl -s "https://get.sdkman.io" | bash

RUN bash -c "source $HOME/.sdkman/bin/sdkman-init.sh && \
    yes | sdk install java 8.0.302-open && \
    yes | sdk install java 11.0.21-tem && \
    yes | sdk install maven 3.9.6 && \
    rm -rf $HOME/.sdkman/archives/* && \
    rm -rf $HOME/.sdkman/tmp/*"

ENTRYPOINT ["/bin/bash"]
#ENTRYPOINT ["source", "$HOME/.sdkman/bin/sdkman-init.sh"]