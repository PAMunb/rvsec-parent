#FROM ubuntu:22.04
FROM phtcosta/rvandroid:0.0.1

#WORKDIR /opt


#ENV SAPIENZ_HOME=/opt/sapienz
#RUN apt-get update && \
#    apt install -qq -y --no-install-recommends libfreetype6-dev libxml2-dev libxslt1-dev python-dev python-tk && \
#    git clone https://github.com/droidxp/sapienz.git && \
#    cd sapienz && \
#    pip2 install -r requirements.txt
#COPY copyreg.py /usr/local/lib/python2.7/dist-packages/deap/copyreg.py


#RUN cd /tmp && \
#    git clone https://github.com/yzygitzh/Humanoid.git && \
#    rm -Rf Humanoid/.git && \
#    cp -Rf Humanoid/* /opt/rvsec/rv-android/tools/humanoid && \
#    cd /opt/rvsec/rv-android && \
#    . venv/bin/activate && \
#    pip3 install pyflann
#COPY pyflann/pyflann /opt/rvsec/rv-android/venv/lib/python3.10/site-packages/pyflann

ENV STOAT_HOME=/opt/Stoat/Stoat
ENV PYTHONPATH=/opt/uiautomator:$PYTHONPATH
ENV CLASSPATH=$STOAT_HOME/soot-github/lib/soot-develop.jar:$CLASSPATH
#ENV PATH=$STOAT_HOME/bin:$PATH
COPY change_python.sh /opt
WORKDIR /opt
RUN apt-get update && \
    apt install -qq -y --no-install-recommends ruby2.7 build-essential patch ruby-dev zlib1g-dev liblzma-dev && \
	gem install nokogiri && \
	git clone https://github.com/rbonifacio/Stoat.git && \
    git clone https://github.com/xiaocong/uiautomator.git && \
    chmod +x /opt/change_python.sh && \
    /opt/change_python.sh $STOAT_HOME


# sapienz
#RUN cd /opt && apt-get install -y --no-install-recommends libfreetype6-dev libxml2-dev libxslt1-dev python-dev && \
#	git clone https://github.com/droidxp/sapienz.git && \
#	cd sapienz && \
#	pip install -r requirements.txt
#ENV SAPIENZ_HOME /opt/sapienz/








WORKDIR /opt/Stoat/Stoat

#RUN chmod a+x run_experiment.sh

#ENV VIRTUAL_ENV=/opt/rvsec/rv-android/venv
#ENV PYTHONPATH=/opt/rvsec/rv-android:$PYTHONPATH
#ENV PATH="$VIRTUAL_ENV/bin:$PATH"

#RUN mkdir /opt/rvsec/rv-android/apks && \
#    cp /opt/rvsec/rv-android/apks_examples/cryptoapp.apk /opt/rvsec/rv-android/apks/

ENTRYPOINT ["/bin/bash"]
#ENTRYPOINT ["python", "main.py"]
#CMD ["python", "main.py"]
