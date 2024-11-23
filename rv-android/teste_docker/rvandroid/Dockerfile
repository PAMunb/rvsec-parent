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
    python3 -m venv venv && \
    source venv/bin/activate && \
    pip install -r requirements.txt && \
    cd tools/qtesting/src && \
    pip install -r requirements.txt

RUN npm install -g appium@1.22.3 && \
    cd /tmp && git clone https://github.com/H2SO4T/ARES && \
    cp -Rf /tmp/ARES/* /opt/rvsec/rv-android/tools/ares && \
    cd /opt/rvsec/rv-android/tools/ares && \
#    python3 -m venv venv && \
#    . venv/bin/activate && \
    pip install -v --timeout=5000 -r rl_interaction/requirements.txt

#RUN cd /opt/rvsec/rv-android/tools/humanoid && \
#    git clone https://github.com/yzygitzh/Humanoid.git . && \
#    pip install pyflann


VOLUME /opt/rvsec/rv-android/apks
VOLUME /opt/rvsec/rv-android/out
VOLUME /opt/rvsec/rv-android/results


ENTRYPOINT ["/bin/bash"]