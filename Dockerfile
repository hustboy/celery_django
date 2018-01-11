FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir -p /home/chenxi/PycharmProjects/filemanager
WORKDIR /home/chenxi/PycharmProjects/filemanager
ADD requirements.txt /home/chenxi/PycharmProjects/filemanager/
RUN pip3 install -r requirements.txt
RUN apt-get update && apt-get install -y \
  openbsd-inetd \
  telnet \
  lftp \
  net-tools

RUN /etc/init.d/openbsd-inetd restart
ADD . /home/chenxi/PycharmProjects/filemanager/
VOLUME ["/mnt/usb:/mnt/usb"]
