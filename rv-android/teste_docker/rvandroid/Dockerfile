#FROM ubuntu:22.04
FROM phtcosta/android:0.0.1

SHELL ["/bin/bash", "-c"]

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /opt

# https://developer.android.com/studio#command-tools
#RUN apt update && apt -qq -y --no-install-recommends install libx11-6 qemu-system-x86 qemu-kvm qemu-utils telnet iptables bridge-utils iproute2 iputils-ping dnsmasq net-tools cpu-checker lshw && \
#RUN apt update && apt -qq -y --no-install-recommends install python3-pip python3-venv python-is-python3 openjdk-8-jdk maven curl unzip wget zip unzip git libgl1-mesa-glx xvfb && \
RUN source /root/.sdkman/bin/sdkman-init.sh && \
    git clone --branch taint https://github.com/PAMunb/rvsec.git && \
    cd rvsec && mvn clean install -DskipTests -DskipMopAgent && \
    cd /opt && git clone https://github.com/honeynet/droidbot.git && \
    cd droidbot && mv setup.py setup_original.py && \
    sed 's/androguard>=3.4.0a1/androguard==3.4.0a1/g' setup_original.py > setup.py && \
    pip install --upgrade pip && \
    pip install -e . && \
    cd /opt/rvsec/rv-android && \
    pip install virtualenv && python -m venv venv && \
    source venv/bin/activate && \
    pip install -r requirements.txt

ENTRYPOINT ["/bin/bash"]