FROM python:3.6
WORKDIR /usr/local/EvaluationBotServer
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "start.py"]
EXPOSE 8888
