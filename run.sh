docker build -t deletefb . && \
docker run -ti --rm \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    --cap-add=SYS_ADMIN \
    --cap-add=NET_ADMIN \
    --cpuset-cpus 0 \
    --memory 4GB \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -e DISPLAY=unix:0 \
    --device /dev/snd \
    --device /dev/dri \
    -v /dev/shm:/dev/shm  \
    deletefb  -e mail="your@email.com" -e pass="Y0Ur*P4ss" -e url="http://facebook.com/your-username" deletefb:latest 
