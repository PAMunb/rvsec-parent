FROM python:3.10-slim-bullseye

ENV DEBIAN_FRONTEND=noninteractive

SHELL ["/bin/bash", "-c"]

ENV ASPECTJ_HOME=/opt/aspectj
ENV PATH=$ASPECTJ_HOME/bin:/usr/local/bin:/usr/bin:/bin:$PATH

# Install basic packages (including: java, python and maven)
RUN apt-get update && \
    apt install -qq -y --no-install-recommends curl wget zip unzip git nano software-properties-common openjdk-11-jdk \
    maven npm psmisc python2 ruby2.7 gnuplot procps && \
    curl  https://bootstrap.pypa.io/pip/2.7/get-pip.py | python2 && \
    pip2 install virtualenv && \
    apt autoremove -y && \
    apt clean all && \
	rm -rf /var/lib/apt/lists/* && \
	rm -rf /tmp/*

#apt-get install -y python2 && \
#curl  https://bootstrap.pypa.io/pip/2.7/get-pip.py | python2 && \
#pip2 install virtualenv
#python2 -m virtualenv venv2

# Install aspectj
RUN mkdir $ASPECTJ_HOME && \
    wget 'https://www.eclipse.org/downloads/download.php?file=/tools/aspectj/aspectj-1.9.6.jar&r=1' -O aspectj-1.9.6.jar && \
    java -jar aspectj-1.9.6.jar -to $ASPECTJ_HOME && \
    mv $ASPECTJ_HOME/bin/ajc $ASPECTJ_HOME/bin/ajc_original && \
    sed 's/-Xmx64M/-Xmx4096M/g' $ASPECTJ_HOME/bin/ajc_original > $ASPECTJ_HOME/bin/ajc && \
    chmod a+x $ASPECTJ_HOME/bin/ajc && \
    rm aspectj-1.9.6.jar


ENTRYPOINT ["/bin/bash"]