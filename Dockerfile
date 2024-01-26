FROM python:3.11.2

WORKDIR /app

RUN pip install google-auth google-api-python-client google-auth-oauthlib google-auth-httplib2

RUN pip install --upgrade openai

COPY . .

CMD [ "python", "-u","Main.py" ]