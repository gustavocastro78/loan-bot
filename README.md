# Loan Bot

O Loan Bot trata-se de um assistente virtual para assuntos que envolvam crédito pessoal.

Este é apenas um projeto teste.

Atenção: Todos os dados utilizados para o treinamento desse assitente virutal são fictícios, e não devem ser utilizados em contextos reais.

Mais informações podem ser obtidas em: https://gustavocastro78.github.io/loan-bot/

## Instalação

```shell
# Clona o repositório
git clone https://github.com/gustavocastro78/loan-bot.git
cd loan-chatbot

# Constrói o container
docker-compose build
```

## Server
Caso esteja utilizando alguma distro Linux é possível utilizar alguns comandos para facilitar a manipulação do projeto.

Primeiro deve-se conceder permissão de execução para o arquivo "rasa":
```shell
chmod +x bin/rasa
```

Em seguida, será possível se utilizar dos comandos:
```shell
#Levanta o container
bin/rasa up

#Realiza o treinamento do modelo utilizado no chatbot
bin/rasa train

#Levanta o serviço de chatbot, action server e chat websocket
bin/rasa start

#Derruba o container
bin/rasa stop

#Roda testes unitários
bin/rasa test
```

Caso seja necessário executar alguma funcionalidade de dentro do container, basta rodar o comando:
```shell
docker-compose exec rasa /bin/bash
```

## Message Channel
Para interagir com o bot, abra no seu navegador o arquivo:
```shell
chat_client/client.html
```

No caso de solicitação com interação com humano, deve haver alguém no chat de suporte. Para isso, abra no navegador o arquivo:
```shell
chat_client/support.html
```
