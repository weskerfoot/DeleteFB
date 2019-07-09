# docker build -t deletefb . && \
# docker run -ti --rm \
#        -e DISPLAY=$DISPLAY \
#        -v /tmp/.X11-unix:/tmp/.X11-unix \
	# --cap-add=SYS_ADMIN \
	# --cap-add=NET_ADMIN \
	# --cpuset-cpus 0 \
	# --memory 4GB \
	# -v /tmp/.X11-unix:/tmp/.X11-unix \
	# -e DISPLAY=unix:0 \
	# --device /dev/snd \
	# --device /dev/dri \
	# -v /dev/shm:/dev/shm  \
#        deletefb


FROM ubuntu:bionic

# Update and apt install
    # add your own sources.list file here in order to speed up the build
    ADD sources.list /etc/apt/sources.list

    RUN apt-get update &&  \
     apt-get install -y firefox \
     git \
     python3 \
     python3-pip \
     libcanberra-gtk-module \
     curl \ 
     sudo \ 
     vim 

# creating user
    # ENV user username
    # RUN export uid=1000 gid=1000 && \
    # mkdir -p /home/${user} && \
    # echo "${user}:x:${uid}:${gid}:${user},,,:/home/${user}:/bin/bash" >> /etc/passwd && \
    # echo "${user}:x:${uid}:" >> /etc/group && \
    # echo "${user} ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/${user} && \
    # chmod 0440 /etc/sudoers.d/${user} && \
    # chown ${uid}:${gid} -R /home/${user} && \
    # usermod -aG sudo ${user}

# Install Chrome
RUN apt-get update && apt-get install -y \
	apt-transport-https \
	ca-certificates \
	curl \
	gnupg \
	hicolor-icon-theme \
	libcanberra-gtk* \
	libgl1-mesa-dri \
	libgl1-mesa-glx \
	libpango1.0-0 \
	libpulse0 \
	libv4l-0 \
	fonts-symbola \
	--no-install-recommends \
	&& curl -sSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
	&& echo "deb [arch=amd64] https://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google.list \
	&& apt-get update && apt-get install -y \
	google-chrome-stable \
	--no-install-recommends && \
	rm -rf /var/lib/apt/lists/*

COPY local.conf /etc/fonts/local.conf


# delete FB repo install


    RUN pip3 install --user delete-facebook-posts
    RUN pip3 install --user git+https://github.com/weskerfoot/DeleteFB.git
    RUN git clone https://github.com/weskerfoot/DeleteFB.git
    WORKDIR ./DeleteFB
    RUN pip3 install -r requirements.txt
#    RUN pip3 install selenium oathlib attrs pybloom_live
    RUN pip3 install attrs pybloom_live
    RUN pip3 install --user selenium
    CMD python3 -m deletefb.deletefb 