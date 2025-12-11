import telebot
import threading
import time
import os
import sys

# --- CONFIGURAÇÃO ---
TOKEN = "8454309616:AAG0TJjt0Jt4wAod0gCmEm4n4Lc1oYjY2m0" 
bot = telebot.TeleBot(TOKEN)

# Variável para saber com quem estamos falando por último
# (Para o bot saber pra quem mandar sua resposta)
ultimo_chat_id = None
ultimo_nome = "Ninguém"

print("\033[1;32m--- SISTEMA DE CHAT DEBIAN ONLINE ---\033[0m")
print("Aguardando mensagens... (Pode digitar a qualquer momento)")

# --- PARTE 1: ESCUTAR O TELEGRAM (Roda em segundo plano) ---

# Receber Texto
@bot.message_handler(func=lambda m: True)
def receber_texto(message):
    global ultimo_chat_id, ultimo_nome
    ultimo_chat_id = message.chat.id
    ultimo_nome = message.from_user.first_name
    
    # Pula uma linha, mostra a mensagem colorida e restaura o prompt
    print(f"\n\r\033[1;36m[{ultimo_nome}]:\033[0m {message.text}")
    print("\r\033[1;32mVocê > \033[0m", end="", flush=True)

# Receber Arquivos (Salva automaticamente)
@bot.message_handler(content_types=['document', 'photo', 'audio', 'video'])
def receber_arquivo(message):
    global ultimo_chat_id, ultimo_nome
    ultimo_chat_id = message.chat.id
    ultimo_nome = message.from_user.first_name

    try:
        if message.content_type == 'document':
            file_id = message.document.file_id
            nome = message.document.file_name
        elif message.content_type == 'photo':
            file_id = message.photo[-1].file_id
            nome = f"foto_{file_id}.jpg"
        else:
            file_id = getattr(message, message.content_type).file_id
            nome = f"{message.content_type}_{file_id}"

        file_info = bot.get_file(file_id)
        downloaded = bot.download_file(file_info.file_path)

        with open(nome, 'wb') as new_file:
            new_file.write(downloaded)

        print(f"\n\r\033[1;33m[ARQUIVO RECEBIDO de {ultimo_nome}]: {nome} salvo!\033[0m")
        bot.reply_to(message, f"✅ Recebi o arquivo: {nome}")
        print("\r\033[1;32mVocê > \033[0m", end="", flush=True)

    except Exception as e:
        print(f"\nErro ao baixar arquivo: {e}")

# --- PARTE 2: ENVIAR PELO TERMINAL (Roda no plano principal) ---
def loop_terminal():
    while True:
        try:
            # Fica esperando você digitar algo
            texto = input("\033[1;32mVocê > \033[0m")
            
            # Comandos especiais do terminal
            if texto.lower() in ['sair', 'exit']:
                print("Encerrando chat...")
                os._exit(0) # Mata tudo, inclusive a thread do bot
            
            # Comando para enviar arquivo: upload nome_do_arquivo.pdf
            elif texto.startswith("upload "):
                if not ultimo_chat_id:
                    print("❌ Ninguém falou com você ainda. Não sei pra quem enviar.")
                    continue
                    
                arquivo_nome = texto.split(" ", 1)[1]
                if os.path.exists(arquivo_nome):
                    print(f"Enviando {arquivo_nome} para {ultimo_nome}...")
                    with open(arquivo_nome, 'rb') as doc:
                        bot.send_document(ultimo_chat_id, doc)
                    print("✅ Enviado!")
                else:
                    print("❌ Arquivo não encontrado na pasta.")

            # Mensagem normal de texto
            else:
                if ultimo_chat_id:
                    bot.send_message(ultimo_chat_id, texto)
                else:
                    print("⚠️ Aguarde alguém mandar um 'Oi' primeiro para responder.")

        except Exception as e:
            print(f"Erro no terminal: {e}")

# --- INICIAR TUDO ---
# Cria uma thread separada para o bot ficar ouvindo sem travar o terminal
thread_bot = threading.Thread(target=bot.infinity_polling)
thread_bot.daemon = True
thread_bot.start()

# O terminal assume o controle agora
loop_terminal()
