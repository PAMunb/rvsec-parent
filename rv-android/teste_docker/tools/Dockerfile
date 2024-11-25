#FROM ubuntu:22.04
FROM phtcosta/rvandroid:0.0.1

WORKDIR /opt

#RUN cd /opt/rvsec/rv-android/tools/qtesting && \
#    python -m venv venv && \
#    source venv/bin/activate && \
#    pip install -r src/requirements.txt



RUN cd /tmp && \
    git clone https://github.com/yzygitzh/Humanoid.git && \
    rm -Rf Humanoid/.git && \
    cp -Rf Humanoid/* /opt/rvsec/rv-android/tools/humanoid && \
    cd /opt/rvsec/rv-android && \
    . venv/bin/activate && \
    pip3 install pyflann

COPY pyflann/pyflann /opt/rvsec/rv-android/venv/lib/python3.10/site-packages/pyflann

ENTRYPOINT ["/bin/bash"]