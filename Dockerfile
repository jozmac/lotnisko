FROM python:3

# COPY /tmp /tmp
COPY . .
# Copy your python program to docker image here 

RUN apt-get update 
RUN apt-get install -y libsm6 libxext6 libfontconfig1 libxrender1 libgl1-mesa-dev libxkbcommon-x11-0 libdbus-1-3 libxcb-cursor0 libxcb-icccm4 libxcb-keysyms1 libxcb-shape0

# Install required python3 packages (add required packages to dependencies.txt file)
RUN pip install -r /dependencies.txt

CMD [ "bash" ]

# First install X11 system for your PC, follow this instruction:
#   https://cuneyt.aliustaoglu.biz/en/running-gui-applications-in-docker-on-windows-linux-mac-hosts/?fbclid=IwAR2O6YImfvcmtq1dEa8cbU8slOM3Q_w2ZvcmulOpF4wPWa0MIL3il9leUHQ

# Build docker image command:
#   docker build -t lotnisko-docker .

#   docker run --rm -it -v /.X11-unix:/.X11-unix -e DISPLAY=192.168.100.26:0 lotnisko-docker
# python /main.py

#   docker run --rm -it -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=192.168.100.26:0 pyqt6-docker python /main.py






# Build docker image command:
#   docker build -t pyqt6-docker .

# Run docker container and enter to it:
#   docker run --rm -it -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=<ip_address>:0 pyqt6-docker
# Note: replace ip_address with host ip i.e. 192.168.1.20

# Run docker container and execute python hello.py program:
#   docker run --rm -it -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=<ip_address>:0 pyqt6-docker python /tmp/hello.py

# python /tmp/hello.py



# FROM python:3.11-bullseye

# ADD hello.py .

# # # Install system-level dependencies
# # RUN apt-get update && apt-get install -y \
# #     <system-level-packages>

# # # Set the working directory inside the container
# # WORKDIR /app

# # # Copy your project files into the container
# # COPY . /app

# RUN pip install PyQt6

# # COPY requirements.txt
# # COPY ./src ./src
# # RUN pip install -r requirements.txt

# # CMD [ "python", "./main.py" ]
# # CMD [ "sh" ]

# # docker build -t lotnisko-docker .
# # docker run lotnisko-docker    

# # docker run --rm -it -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=192.168.100.26:0 -u qtuser jozo/pyqt5 python3 /tmp/hello.py
# # docker image list
# # docker continer list