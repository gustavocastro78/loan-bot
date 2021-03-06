#Utiliza a imagem do python 3.7.9
FROM python:3.7.9-slim

#Cria diretorios /home/src
RUN mkdir -p /home/loan-bot/src

#Define a área de trabalho
WORKDIR /home/loan-bot

#Copia as dependencias locais para o container
COPY requirements.txt requirements.txt

#Cria ambiente
RUN python -m venv venv

#Atualiza pip
RUN pip3 install --upgrade pip

#Instala as dependencias
RUN pip3 install -r requirements.txt

#Instala módulos pré-treinados
RUN python -m spacy download pt_core_news_sm
RUN python -m spacy link pt_core_news_sm pt

#Copia todos os arquivos para o container
COPY . .
