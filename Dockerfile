FROM ubuntu:18.04

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

COPY ./requirements.txt /NTIDiscordBot/requirements.txt

WORKDIR /NTIDiscordBot

#RUN python -m venv env

RUN pip install -U -r requirements.txt

COPY . /NTIDiscordBot

ENTRYPOINT [ "python" ]

CMD [ "main.py" ]