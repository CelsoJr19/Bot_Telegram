import telebot
import threading
import time
import os
import sys

# --- CONFIGURAÇÃO ---
TOKEN = "8454309616:AAG0TJjt0Jt4wAod0gCmEm4n4Lc1oYjY2m0" 
bot = telebot.TeleBot(TOKEN)

# --- LISTA DE CONTATOS ---
# Adicione aqui os IDs dos seus amigos para dar apelidos
AMIGOS = {
    # Exemplo: 12345678: "Melhor Amigo",
}

# --- CORES E VISUAL ---
COR_AZUL = "\033[1;34m"   # Azul escuro
COR_CIANO = "\033[1;36m"  # Azul claro
COR_BRANCO = "\033[1;37m" # Branco brilhante
COR_RESET = "\033[0m"

def mostrar_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    logo = fr"""
    {COR_AZUL}      _______
    {COR_AZUL}    /  ____  \
    {COR_AZUL}   /  |    |  \    {COR_CIANO} _____ _____ _      _____ _____ _____  ___  ___
    {COR_AZUL}  |   |____|   |   {COR_CIANO}|_   _|   __| |    |   __|   __| __  ||   ||   |
    {COR_AZUL}   \          /    {COR_CIANO}  | | |   __| |___ |   __|   __|    -|| | || | |
    {COR_AZUL}    \________/     {COR_CIANO}  |_| |_____|_____||_____|_____|__|__||___||_|_|

    {COR_RESET}   >>> Server Online • Debian 32-bit • v2.0 <<<
    """
    print(logo)

def obter_nome_formatado(message):
    id_user = message.chat.id
    nome_original = message.from_user.first_name
    
    # Se conhecemos o ID, usamos o apelido
    if id_user in AMIGOS:
        return f"\033[1;35m{AMIGOS[id_user]}\033[0m" # Cor Rosa para VIPs
    
    # Se não, mostra o nome original + ID (pra você copiar)
    return f"{nome_original} \033[90m(ID: {id_user})\033[0m"

# Variáveis Globais
ultimo_chat_id = None
ultimo_nome = "Ninguém"

mostrar_banner()
print(f"{COR_BRANCO}Aguardando conexões... (Ctrl+C para encerrar){COR_RESET}\n")

# --- RECEBER TEXTO ---
@bot.message_handler(func=lambda m: True)
def receber_texto(message):
    global ultimo_chat_id, ultimo_nome
    ultimo_chat_id = message.chat.id
    ultimo_nome = obter_nome_formatado(message)
    
    print(f"\n\r\033[1;36m[{ultimo_nome}]:\033[0m {message.text}")
    print("\r\033[1;32mVocê > \033[0m", end="", flush=True)

# --- RECEBER ARQUIVOS ---
@bot.message_handler(content_types=['document', 'photo', 'audio', 'video'])
def receber_arquivo(message):
    global ultimo_chat_id, ultimo_nome
    ultimo_chat_id = message.chat.id
    ultimo_nome = obter_nome_formatado(message)

    try:
        # Lógica para pegar o ID do arquivo
        if message.content_type == 'document':
            file_id = message.document.file_id
            nome = message.document.file_name
        elif message.content_type == 'photo':
            file_id = message.photo[-1].file_id
            nome = f"foto_{file_id[-5:]}.jpg" # Nome curto
        else:
            file_id = getattr(message, message.content_type).file_id
            nome = f"{message.content_type}_{file_id[-5:]}"

        file_info = bot.get_file(file_id)
        downloaded = bot.download_file(file_info.file_path)

        with open(nome, 'wb') as new_file:
            new_file.write(downloaded)

        print(f"\n\r\033[1;33m[ARQUIVO DE {ultimo_nome}]: {nome} salvo!\033[0m")
        bot.reply_to(message, f"✅ Recebi: {nome}")
        print("\r\033[1;32mVocê > \033[0m", end="", flush=True)

    except Exception as e:
        print(f"\nErro download: {e}")

# --- ENVIAR ---
def loop_terminal():
    while True:
        try:
            texto = input("\033[1;32mVocê > \033[0m")
            
            if texto.lower() in ['sair', 'exit']:
                os._exit(0)
            
            elif texto.startswith("upload "):
                if not ultimo_chat_id:
                    print("❌ Ninguém falou com você ainda.")
                    continue
                arquivo = texto.split(" ", 1)[1]
                if os.path.exists(arquivo):
                    print(f"Enviando {arquivo}...")
                    with open(arquivo, 'rb') as doc:
                        bot.send_document(ultimo_chat_id, doc)
                else:
                    print("❌ Arquivo não existe.")
            else:
                if ultimo_chat_id:
                    bot.send_message(ultimo_chat_id, texto)
                else:
                    print("⚠️ Espere alguém mandar mensagem primeiro.")

        except Exception as e:
            print(f"Erro: {e}")

# --- START ---
t = threading.Thread(target=bot.infinity_polling)
t.daemon = True
t.start()
loop_terminal()
