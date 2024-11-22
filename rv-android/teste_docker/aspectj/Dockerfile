FROM phtcosta/sdkman:0.0.1

SHELL ["/bin/bash", "-c"]

ENV DEBIAN_FRONTEND=noninteractive

#ARG ASPECTJ_VERSION=1.9.6

ENV ASPECTJ_HOME=/aspectj
ENV PATH=/aspectj/bin:$PATH

RUN source ${HOME}/.sdkman/bin/sdkman-init.sh &&  \
    mkdir /aspectj && \
    wget 'https://www.eclipse.org/downloads/download.php?file=/tools/aspectj/aspectj-1.9.6.jar&r=1' -O aspectj-1.9.6.jar && \
    java -jar aspectj-1.9.6.jar -to aspectj && \
    mv /aspectj/bin/ajc /aspectj/bin/ajc_original && \
    sed 's/-Xmx64M/-Xmx4096M/g' /aspectj/bin/ajc_original > /aspectj/bin/ajc && \
    chmod a+x /aspectj/bin/ajc && \
    rm aspectj-1.9.6.jar
