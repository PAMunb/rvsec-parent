#FROM ubuntu:22.04
FROM phtcosta/aspectj:0.0.1

SHELL ["/bin/bash", "-c"]

ENV DEBIAN_FRONTEND=noninteractive

# Arguments that can be overriden at build-time.
ARG INSTALL_ANDROID_SDK=1
ARG API_LEVEL=29
ARG IMG_TYPE=google_apis
#ARG ARCHITECTURE=x86_64
ARG ARCHITECTURE=x86
#ARG CMD_LINE_VERSION=11076708_latest
ARG CMD_LINE_VERSION=8512546_latest
ARG DEVICE_ID=pixel
ARG GPU_ACCELERATED=false

ENV PACKAGE_PATH="system-images;android-${API_LEVEL};${IMG_TYPE};${ARCHITECTURE}"
ENV ANDROID_PLATFORM_VERSION="platforms;android-$API_LEVEL"
ENV ANDROID_SDK_PACKAGES="${PACKAGE_PATH} ${ANDROID_PLATFORM_VERSION} platform-tools build-tools;34.0.0"

ENV EMULATOR_NAME="RVSec"
ENV ANDROID_HOME=/opt/android
ENV ANDROID_SDK_ROOT=/opt/android
ENV PATH=$ANDROID_HOME/platform-tools:$ANDROID_HOME/cmdline-tools/tools/bin:$ANDROID_HOME/emulator:$ANDROID_HOME/build-tools/34.0.0:$PATH
ENV LD_LIBRARY_PATH="$ANDROID_SDK_ROOT/emulator/lib64:$ANDROID_SDK_ROOT/emulator/lib64/qt/lib"

ENV API_LEVEL=$API_LEVEL \
	DEVICE_ID=$DEVICE_ID \
	ARCHITECTURE=$ARCHITECTURE \
	ABI=${IMG_TYPE}/${ARCHITECTURE} \
	GPU_ACCELERATED=$GPU_ACCELERATED \
	QTWEBENGINE_DISABLE_SANDBOX=1 \
	ANDROID_EMULATOR_WAIT_TIME_BEFORE_KILL=10 \
	ANDROID_AVD_HOME=/data

WORKDIR /opt

# Create fake keymap file
RUN mkdir -v -p $ANDROID_SDK_ROOT/tools/keymaps && \
    touch $ANDROID_SDK_ROOT/tools/keymaps/en-us


# Initializing the required directories.
RUN mkdir /root/.android/ &&  \
    touch /root/.android/repositories.cfg && \
	mkdir /data

COPY license_accepter.sh /opt/android/license_accepter.sh
# Exporting ADB keys.
COPY keys/* /root/.android/


# The following layers will download the Android command-line tools
# to install the Android SDK, emulator and system images.
# It will then install the Android SDK and emulator.
#COPY scripts/install-sdk.sh /opt/
#RUN chmod +x /opt/install-sdk.sh
#
#
## Copy the container scripts in the image.
#COPY scripts/start-emulator.sh /opt/
#COPY scripts/emulator-monitoring.sh /opt/
#RUN chmod +x /opt/*.sh



# https://developer.android.com/studio#command-tools
#RUN apt update && apt -qq -y --no-install-recommends install libx11-6 qemu-system-x86 qemu-kvm qemu-utils telnet iptables bridge-utils iproute2 iputils-ping dnsmasq net-tools cpu-checker lshw && \
#RUN apt update && apt -qq -y --no-install-recommends install python3-pip python3-venv python-is-python3 openjdk-8-jdk maven curl unzip wget zip unzip git libgl1-mesa-glx xvfb && \
RUN source /root/.sdkman/bin/sdkman-init.sh && \
    apt update && apt -qq -y --no-install-recommends install python3-pip python3-venv bzip2 libdrm-dev \
	libxkbcommon-dev libgbm-dev libasound-dev libnss3 \
	libxcursor1 libpulse-dev libxshmfence-dev \
	xauth xvfb x11vnc fluxbox wmctrl libdbus-glib-1-2 socat \
	virt-manager && \
    wget https://dl.google.com/android/repository/commandlinetools-linux-${CMD_LINE_VERSION}.zip -P /tmp && \
    mkdir $ANDROID_SDK_ROOT/cmdline-tools/ && \
    unzip -d $ANDROID_SDK_ROOT/cmdline-tools/ /tmp/commandlinetools-linux-${CMD_LINE_VERSION}.zip && \
    mv $ANDROID_SDK_ROOT/cmdline-tools/cmdline-tools/ $ANDROID_SDK_ROOT/cmdline-tools/tools/ && \
    rm /tmp/commandlinetools-linux-${CMD_LINE_VERSION}.zip && \
    yes Y | sdkmanager --licenses && \
    sdkmanager --install ${ANDROID_SDK_PACKAGES} && \
#    yes Y | sdkmanager --verbose --no_https ${ANDROID_SDK_PACKAGES} && \
#    echo "no" | avdmanager --verbose create avd --force --name "${EMULATOR_NAME}" --device "pixel" --package "${PACKAGE_PATH}" && \
    echo "no" | avdmanager --verbose create avd --force --name "${EMULATOR_NAME}" --abi "$ABI" --package "$PACKAGE_PATH" --device "$DEVICE_ID"
#    chmod +x /opt/android/license_accepter.sh && ./opt/android/license_accepter.sh $ANDROID_SDK_ROOT

WORKDIR /opt/rvsec/rv-android

ENTRYPOINT ["/bin/bash"]