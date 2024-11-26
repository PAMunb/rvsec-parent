#FROM ubuntu:22.04
FROM phtcosta/rvandroid:0.0.1

#WORKDIR /opt

#RUN cd /opt/rvsec/rv-android/tools/qtesting && \
#    python -m venv venv && \
#    source venv/bin/activate && \
#    pip install -r src/requirements.txt

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

WORKDIR /opt/rvsec/rv-android

#RUN chmod a+x run_experiment.sh

CMD ["run_experiment.sh"]
