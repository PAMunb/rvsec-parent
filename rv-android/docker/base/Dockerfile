FROM python:3.10-slim-bullseye

ENV DEBIAN_FRONTEND=noninteractive

SHELL ["/bin/bash", "-c"]

ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV ASPECTJ_HOME=/opt/aspectj
ENV PATH=$ASPECTJ_HOME/bin:$JAVA_HOME/bin:$PATH

# Install basic packages (including: java, python and maven)
RUN apt-get update && \
    apt install -qq -y --no-install-recommends curl wget zip unzip git nano software-properties-common \
    openjdk-11-jdk maven npm psmisc procps && \
    apt autoremove -y && \
    apt clean all && \
	rm -rf /var/lib/apt/lists/* && \
	rm -rf /tmp/*

# Install aspectj
RUN mkdir $ASPECTJ_HOME && \
    wget 'https://www.eclipse.org/downloads/download.php?file=/tools/aspectj/aspectj-1.9.6.jar&r=1' -O aspectj-1.9.6.jar && \
    java -jar aspectj-1.9.6.jar -to $ASPECTJ_HOME && \
    sed -i 's/-Xmx64M/-Xmx4096M/g' $ASPECTJ_HOME/bin/ajc && \
    chmod a+x $ASPECTJ_HOME/bin/ajc && \
    rm aspectj-1.9.6.jar
