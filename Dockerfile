# hello
FROM ubuntu:22.04

RUN apt-get update -y
RUN apt-get install -y python3 python3-dev python3-pip

# https://ubuntu.com/security/cves?q=&package=&priority=high&version=focal&status=&offset=0
# CVE-2023-6176 | High | linux-azure | Needed
# RUN apt-get install -y linux-azure
WORKDIR /src

COPY . .

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install poetry
RUN poetry install

ENTRYPOINT ["trivy-test-ghas"] 