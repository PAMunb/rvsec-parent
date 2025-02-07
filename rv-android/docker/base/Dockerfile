FROM python:3.10.16-slim-bookworm

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Sao_Paulo

SHELL ["/bin/bash", "-c"]

ENV JAVA_HOME=/opt/openjdk-21.0.2
ENV RV_RT_JAR=/opt/java-se-8u44-ri/jre/lib/rt.jar
ENV MAVEN_HOME=/opt/apache-maven-3.9.9
ENV ASPECTJ_HOME=/opt/aspectj
ENV PATH=$ASPECTJ_HOME/bin:$JAVA_HOME/bin:$MAVEN_HOME/bin:$PATH

# Install basic packages
RUN apt update && \
    apt upgrade && \
    apt install -qq -y --no-install-recommends curl wget zip unzip git nano software-properties-common

WORKDIR /opt

# Install java 21
RUN wget https://download.java.net/java/GA/jdk21.0.2/f2283984656d49d69e91c558476027ac/13/GPL/openjdk-21.0.2_linux-x64_bin.tar.gz && \
    tar -xzf openjdk-21.0.2_linux-x64_bin.tar.gz && \
    mv jdk-21.0.2 openjdk-21.0.2 && \
    rm openjdk-21.0.2_linux-x64_bin.tar.gz

# Download java (jre) 8
RUN wget https://download.java.net/openjdk/jdk8u44/ri/openjdk-8u44-linux-x64.tar.gz && \
    tar -xzf openjdk-8u44-linux-x64.tar.gz && \
    rm -Rf java-se-8u44-ri/sample java-se-8u44-ri/src.zip java-se-8u44-ri/demo && \
    rm openjdk-8u44-linux-x64.tar.gz

# Install maven
RUN wget https://dlcdn.apache.org/maven/maven-3/3.9.9/binaries/apache-maven-3.9.9-bin.zip && \
    unzip apache-maven-3.9.9-bin.zip && \
    rm apache-maven-3.9.9-bin.zip

# Install aspectj
RUN mkdir $ASPECTJ_HOME && \
    wget 'https://www.eclipse.org/downloads/download.php?file=/tools/aspectj/aspectj-1.9.6.jar&r=1' -O aspectj-1.9.6.jar && \
    java -jar aspectj-1.9.6.jar -to $ASPECTJ_HOME && \
    sed -i 's/-Xmx64M/-Xmx4096M/g' $ASPECTJ_HOME/bin/ajc && \
    chmod a+x $ASPECTJ_HOME/bin/ajc && \
    rm aspectj-1.9.6.jar

# Clear
RUN apt autoremove -y && \
    apt clean all && \
	rm -rf /var/lib/apt/lists/* && \
	rm -rf /tmp/*
