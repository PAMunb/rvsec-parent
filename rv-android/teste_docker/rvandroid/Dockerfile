#FROM ubuntu:22.04
FROM phtcosta/rvsec_android:0.0.1

WORKDIR /opt

# https://developer.android.com/studio#command-tools
#RUN apt update && apt -qq -y --no-install-recommends install libx11-6 qemu-system-x86 qemu-kvm qemu-utils telnet iptables bridge-utils iproute2 iputils-ping dnsmasq net-tools cpu-checker lshw && \
#RUN apt update && apt -qq -y --no-install-recommends install python3-pip python3-venv python-is-python3 openjdk-8-jdk maven curl unzip wget zip unzip git libgl1-mesa-glx xvfb && \
RUN git clone https://github.com/honeynet/droidbot.git && \
    cd droidbot && \
    mv setup.py setup_original.py && \
    sed 's/androguard>=3.4.0a1/androguard==3.4.0a1/g' setup_original.py > setup.py && \
    pip3 install -e .

RUN cd /opt && \
    git clone --branch taint https://github.com/PAMunb/rvsec.git && \
    cd rvsec && \
    mvn clean install -DskipTests -DskipMopAgent && \
    cd /opt/rvsec/rv-android && \
    mvn clean compile && \
    python -m venv venv && \
    . venv/bin/activate && \
    pip3 install -r requirements.txt && \
    cd /opt/rvsec/rv-android/tools/qtesting && \
    pip3 install -r src/requirements.txt

#RUN cd /opt/rvsec/rv-android/tools/qtesting && \
#    python -m venv venv && \
#    source venv/bin/activate && \
#    pip install -r src/requirements.txt

ENV PYTHONPATH=/opt/rvsec/rv-android/tools/ares
RUN npm install -g appium@1.22.3 && \
    cd /tmp && git clone https://github.com/H2SO4T/ARES && \
    cp -Rf /tmp/ARES/* /opt/rvsec/rv-android/tools/ares && \
    cd /opt/rvsec/rv-android/tools/ares && \
    python -m venv venv && \
    . venv/bin/activate && \
    pip install -v --timeout=5000 -r rl_interaction/requirements.txt

#RUN cd /opt/rvsec/rv-android/tools/humanoid && \
#    git clone https://github.com/yzygitzh/Humanoid.git . && \
#    pip install pyflann

RUN apt autoremove -y && \
    apt clean all && \
	rm -rf /var/lib/apt/lists/* && \
	rm -rf /tmp/*


ENV RV_REPETITIONS=1
ENV RV_TIMEOUTS=60
ENV RV_TOOLS=monkey
ENV RV_HUMANOID_URL=127.0.0.1:50405
ENV RV_SKIP_MONITORS=false
ENV RV_SKIP_INSTRUMENT=false
ENV RV_SKIP_STATIC_ANALYSIS=false
ENV ENV_SKIP_EXPERIMENT=false
ENV ENV_NO_WINDOW=true

#TODO receber o dir das specs tbm?

VOLUME /opt/rvsec/rv-android/apks
VOLUME /opt/rvsec/rv-android/out
VOLUME /opt/rvsec/rv-android/results

WORKDIR /opt/rvsec/rv-android

ENV PATH=/opt/rvsec/rv-android/venv/bin:$PATH

#ENTRYPOINT ["/bin/bash"]
#CMD ["run_experiment.sh"]
CMD ["python", "main.py"]