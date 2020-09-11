FROM python:3
WORKDIR /home/fedresurs
COPY . ./
RUN [ "pip", "install", "-r", "requirements.txt" ]
EXPOSE 5000
ENTRYPOINT [ "python", "run.py" ]