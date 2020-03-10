FROM python:latest



WORKDIR "/root/Bulk Downloader for Reddit"
COPY ./requirements.txt ./
RUN ["pip", "install", "-r", "requirements.txt"]
EXPOSE 8080

CMD ["python", "script.py", "-d", "downloads"]  