# to build and launch, edit ./run.sh
# with your values, then execute it

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

#creating user
    ENV user username
    RUN export uid=1000 gid=1000 && \
    mkdir -p /home/${user} && \
    echo "${user}:x:${uid}:${gid}:${user},,,:/home/${user}:/bin/bash" >> /etc/passwd && \
    echo "${user}:x:${uid}:" >> /etc/group && \
    echo "${user} ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/${user} && \
    chmod 0440 /etc/sudoers.d/${user} && \
    chown ${uid}:${gid} -R /home/${user} && \
    usermod -aG sudo ${user}

# delete FB repo install
    USER ${user}
    WORKDIR /home/${user}

    ARG mail  
    ARG pass  
    ARG url  

    RUN pip3 install --user delete-facebook-posts
    RUN pip3 install --user git+https://github.com/weskerfoot/DeleteFB.git
    RUN git clone https://github.com/weskerfoot/DeleteFB.git 
    RUN pip3 install -r ./DeleteFB/requirements.txt
    RUN pip3 install --user selenium attrs pybloom_live
    CMD python3 -m deletefb.deletefb -E ${mail} -P ${pass} -U ${url}  