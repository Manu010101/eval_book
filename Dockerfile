FROM python:3.6-alpine3.7

COPY main.py .
COPY BD.py .
COPY Glob.py .
COPY Oddsportal.py .

# installation de chromedriver
RUN apk update
RUN apk add chromium chromium-chromedriver

ENV DISPLAY=:99

RUN pip install selenium
RUN pip install matplotlib

CMD ["python", "./main.py"]
