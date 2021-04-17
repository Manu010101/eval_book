FROM czentye/matplotlib-minimal

COPY main.py .
COPY BD.py .
COPY Glob.py .
COPY Oddsportal.py .

# installation de chromedriver
RUN apk update
RUN apk add chromium chromium-chromedriver

ENV DISPLAY=:99


RUN pip install selenium
RUN pip install typing

CMD ["python", "./main.py"]
