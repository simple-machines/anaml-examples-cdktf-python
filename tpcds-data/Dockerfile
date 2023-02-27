FROM ubuntu
RUN apt-get update && apt-get install -y gcc make flex bison byacc
RUN mkdir /data
ADD tools /opt/tools
WORKDIR /opt/tools
RUN make OS=LINUX
RUN chmod +x dsdgen
ENTRYPOINT [ "dsdgen" ]
CMD [ "-SCALE", "1", "-DIR", "/data" ]
