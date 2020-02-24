FROM python:3.8.1

COPY . /Sentiment-Analysis

WORKDIR /Sentiment-Analysis

RUN pip install -r requirements.txt

CMD ["python3","api.py"]