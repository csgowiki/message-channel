FROM python:3.8.10-alpine
COPY ./ ./
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories &&\
    apk add gcc musl-dev g++ zlib-dev make &&\
    pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple