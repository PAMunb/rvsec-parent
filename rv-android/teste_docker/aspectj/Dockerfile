FROM phtcosta/rvsec_base:0.0.1

ENV ASPECTJ_HOME=/opt/aspectj
ENV PATH=$ASPECTJ_HOME/bin:$PATH

RUN mkdir $ASPECTJ_HOME && \
    wget 'https://www.eclipse.org/downloads/download.php?file=/tools/aspectj/aspectj-1.9.6.jar&r=1' -O aspectj-1.9.6.jar && \
    java -jar aspectj-1.9.6.jar -to $ASPECTJ_HOME && \
    mv $ASPECTJ_HOME/bin/ajc $ASPECTJ_HOME/bin/ajc_original && \
    sed 's/-Xmx64M/-Xmx4096M/g' $ASPECTJ_HOME/bin/ajc_original > $ASPECTJ_HOME/bin/ajc && \
    chmod a+x $ASPECTJ_HOME/bin/ajc && \
    rm aspectj-1.9.6.jar
