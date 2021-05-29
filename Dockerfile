FROM alpine:3.8

ENV JAVA_HOME="/usr/lib/jvm/default-jvm/"
ENV PATH=$PATH:${JAVA_HOME}/bin
ENV PYTHONUNBUFFERED=1

RUN apk update && \
    apk upgrade 
RUN apk add --no-cache openjdk8 ruby curl python3 pdftk ruby-rdoc && \
    gem install asciidoctor-pdf

WORKDIR /opt/swagger2pdf

RUN curl https://repo1.maven.org/maven2/io/swagger/codegen/v3/swagger-codegen-cli/3.0.24/swagger-codegen-cli-3.0.24.jar > swagger-codegen-cli.jar && \
    chmod +x swagger-codegen-cli.jar
RUN curl -L https://github.com/Irdis/SwDoc/raw/master/swaggercli/swagger2markup-cli-2.0.0-SNAPSHOT.jar > swagger2markup-cli.jar && \
    chmod +x swagger2markup-cli.jar

COPY app ./

ENTRYPOINT ["python3", "swagger-export.py"]