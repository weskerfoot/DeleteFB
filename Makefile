# Makefile

NAME:= deletefb

.PHONY: all build run

all:  build run

build:
	@docker build -t $(NAME) .   

run:
	@read -p "Enter your Facebook email: " email && read -p "Enter your Facebook password: " password && read -p "Enter your Facebook username: " username  && docker run -ti --rm \
    -e DISPLAY=$$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    --cap-add=SYS_ADMIN \
    --cap-add=NET_ADMIN \
    --cpuset-cpus 0 \
    --device /dev/dri \
    -v /dev/shm:/dev/shm  \
    -e EMAIL="$$email" \
    -e PASS="$$password" \
    -e URL="https://facebook.com/$$username" \
    $(NAME):latest