FROM python:latest

WORKDIR "/root/Bulk Downloader for Reddit"
COPY ./requirements.txt ./
RUN ["pip", "install", "-r", "requirements.txt"]
EXPOSE 8080
EXPOSE 1337

CMD ["python", "script.py", "-d", "downloads"]  