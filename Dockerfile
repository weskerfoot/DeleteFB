# To run, just type "make", or 

# docker build -t deletefb . 
# docker run -ti --rm \
#     -e DISPLAY=$DISPLAY \
#     -v /tmp/.X11-unix:/tmp/.X11-unix \
#     --cap-add=SYS_ADMIN \
#     --cap-add=NET_ADMIN \
#     --cpuset-cpus 0 \
#     --memory 4GB \
#     -v /tmp/.X11-unix:/tmp/.X11-unix \
#     -e DISPLAY=unix:0 \
#     --device /dev/snd \
#     --device /dev/dri \
#     -v /dev/shm:/dev/shm  \
#     deletefb  -e mail="your@email.com" -e pass="Y0Ur*P4ss" -e url="http://facebook.com/your-username" deletefb:latest

FROM debian:stable-slim
    
    RUN apt-get update &&  \
     apt-get install -y \
     git \
     python3 \
     python3-pip \
     libcanberra-gtk-module \
     curl \ 
     sudo \ 
     vim  \
     unzip \
     chromium \
     chromium-driver

#creating new user
    ENV user deletefb
    RUN export uid=1000 gid=1000 && \
    mkdir -p /home/${user} && \
    echo "${user}:x:${uid}:${gid}:${user},,,:/home/${user}:/bin/bash" >> /etc/passwd && \
    echo "${user}:x:${uid}:" >> /etc/group && \
    echo "${user} ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/${user} && \
    chmod 0440 /etc/sudoers.d/${user} && \
    chown ${uid}:${gid} -R /home/${user} && \
    usermod -aG sudo ${user}


# deletefb install
    USER ${user}
    WORKDIR /home/${user}
    
    ARG email  
    ARG pass  
    ARG url  
    #ARG --conversations

    RUN pip3 install --user delete-facebook-posts
    RUN pip3 install --user selenium attrs pybloom_live

    ADD run.sh /tmp/run.sh
    ENTRYPOINT [ "/tmp/run.sh" ]
