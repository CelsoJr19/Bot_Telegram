# Bot_Telegram
API de Bot do Telegram para usar o telegram no meu computador Headless de 32 Bits para poder converar, mandar e receber arquivos de seus amigos.

# Passo 1: Criar o Bot (No seu celular)
Você precisa "registrar" o bot no Telegram para ganhar a chave de acesso.
Abra o Telegram no seu celular.
Procure pelo usuário @BotFather (é o bot oficial que cria outros bots).
Mande a mensagem: /newbot
Ele vai pedir um Nome (ex: Notebook do Celso).
Ele vai pedir um Username (tem que terminar em bot, ex: celso_debian_bot).
O BotFather vai te dar um TOKEN (uma chave longa cheia de números e letras). Copie esse Token.

# Passo 2: Preparar o Ambiente no Linux
Instale a biblioteca:
_pip install pyTelegramBotAPI_

Crie uma pasta para o projeto:
_cd ~
mkdir telegram_bot
cd telegram_bot
python3 -m venv venv
source venv/bin/activate_

Baixe o código .py e coloque-o nessa pasta, edite o código para poder colocar o seu Token do telegram e editar sua lista de amigos colocando o ID deles e o apelido
Obs: Caso não saiba o ID, pessa para que mandem mensagem ao seu bot do telegram e o ID aparecerá no chat do linux.
