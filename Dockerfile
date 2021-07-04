FROM python:3.8-slim
WORKDIR /
ADD requirements.txt /
RUN pip3 install -r requirements.txt
ADD . /
EXPOSE 5000
ENTRYPOINT ["python", "app.py"]