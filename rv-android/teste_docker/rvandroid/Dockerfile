FROM phtcosta/rvsec_android:0.0.1

WORKDIR /opt
RUN git clone https://github.com/honeynet/droidbot.git && \
    cd droidbot && \
    mv setup.py setup_original.py && \
    sed 's/androguard>=3.4.0a1/androguard==3.4.0a1/g' setup_original.py > setup.py && \
    pip3 install -e .


#ENV VIRTUAL_ENV=/opt/rvsec/rv-android/venv
WORKDIR /opt/rvsec
RUN git clone --branch taint https://github.com/PAMunb/rvsec.git . && \
    mvn clean install -DskipTests -DskipMopAgent && \
    mvn clean compile -f /opt/rvsec/rv-android/pom.xml && \
#    python3 -m venv $VIRTUAL_ENV && \
    pip3 install -r rv-android/requirements.txt && \
    pip3 install -r rv-android/tools/qtesting/src/requirements.txt
#ENV PATH="$VIRTUAL_ENV/bin:$PATH"


WORKDIR /tmp
ENV PYTHONPATH=/opt/rvsec/rv-android/tools/ares
RUN npm install -g appium@1.22.3 && \
    git clone https://github.com/H2SO4T/ARES && \
    cp -Rf /tmp/ARES/* /opt/rvsec/rv-android/tools/ares && \
    cd /opt/rvsec/rv-android/tools/ares && \
    python3 -m venv venv && \
    . venv/bin/activate && \
    pip install -v --timeout=5000 -r rl_interaction/requirements.txt
#rm -Rf /opt/rvsec/rv-android/tools/ares/.git && \


RUN apt autoremove -y && \
    apt clean && \
	rm -rf /var/lib/apt/lists/* && \
	rm -rf /tmp/*


ENV RV_REPETITIONS=1
ENV RV_TIMEOUTS=60
ENV RV_TOOLS=monkey
ENV RV_HUMANOID_URL=humanoid:50405
ENV RV_SKIP_MONITORS=false
ENV RV_SKIP_INSTRUMENT=false
ENV RV_SKIP_STATIC_ANALYSIS=false
ENV RV_SKIP_EXPERIMENT=false
ENV RV_NO_WINDOW=true

#TODO receber o dir das specs tbm?

VOLUME /opt/rvsec/rv-android/apks
VOLUME /opt/rvsec/rv-android/out
VOLUME /opt/rvsec/rv-android/results

WORKDIR /opt/rvsec/rv-android

CMD ["python", "main.py"]
