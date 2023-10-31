
FROM python:3.11-bullseye

ADD main.py .

# # Install system-level dependencies
# RUN apt-get update && apt-get install -y \
#     <system-level-packages>

# # Set the working directory inside the container
# WORKDIR /app

# # Copy your project files into the container
# COPY . /app

RUN pip install PyQt6

# COPY requirements.txt
# COPY ./src ./src
# RUN pip install -r requirements.txt

CMD [ "python", "./main.py" ]


# docker build -t lotnisko-docker .
# docker run lotnisko-docker    