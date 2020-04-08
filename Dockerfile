FROM python:3.7
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
EXPOSE 443
CMD python app.py
