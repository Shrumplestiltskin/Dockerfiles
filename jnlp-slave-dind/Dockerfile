FROM jenkins/jnlp-slave:3.10-1
USER root
RUN apt-get update && apt-get install -y \
   apt-transport-https \
   ca-certificates \
   curl \
   gnupg2 \
   software-properties-common
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -
RUN add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/debian \
   $(lsb_release -cs) \
   stable"
RUN apt-get update && apt-get install -y \
   docker-ce=5:18.09.0~3-0~debian-stretch
RUN usermod -a -G docker jenkins
USER jenkins
