FROM ubuntu
RUN apt-get update && apt-get install -y gcc make flex bison byacc
ADD tools /opt/tools
WORKDIR /opt/tools
RUN make OS=LINUX
