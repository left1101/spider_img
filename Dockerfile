FROM python:3.6.9-alpine3.9

WORKDIR /usr/src/app

RUN  echo "https://mirrors.aliyun.com/alpine/v3.10/main" > /etc/apk/repositories && \
 echo "https://mirrors.aliyun.com/alpine/v3.10/community" >> /etc/apk/repositories && \
 apk add --no-cache gcc musl-dev linux-headers

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["gunicorn", "app:app", "-c", "./gunicorn.conf.py"]
# RUN gunicorn -c gunicorn.conf.py app:app
