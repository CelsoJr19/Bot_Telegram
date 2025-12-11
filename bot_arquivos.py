import telebot
import threading
import os
import sys

# --- CONFIGURAÇÃO ---
TOKEN = "Seu Token aqui" 
bot = telebot.TeleBot(TOKEN)

# --- LISTA DE CONTATOS (SUA AGENDA) ---
# Dica: Peça pro seu amigo mandar um "Oi" primeiro pra descobrir o ID dele.
AMIGOS = {
    # ID : "Apelido"
    123456789: "Teste", #Exemplo
    987654321: "Hugo", #Exemplo
    555555555: "Mae", #Exemplo
    # Adicione seus amigos aqui...
}

# Cores
COR_AZUL = "\033[1;34m"
COR_CIANO = "\033[1;36m"
COR_VERDE = "\033[1;32m"
COR_AMARELO = "\033[1;33m"
COR_ROSA = "\033[1;35m"
COR_RESET = "\033[0m"

# Variáveis Globais
chat_atual_id = None
chat_atual_nome = "Ninguém"

def mostrar_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    logo = fr"""
    {COR_AZUL}  ____ _   _    _  _____ 
    {COR_AZUL} / ___| | | |  / \|_   _|
    {COR_AZUL}| |   | |_| | / _ \ | |  
    {COR_AZUL}| |___|  _  |/ ___ \| |  
    {COR_AZUL} \____|_| |_/_/   \_\_|  
    
    {COR_CIANO} _____ _____ _    _____ ____ ____      _    __  __
    {COR_CIANO}|_   _| ____| |  | ____/ ___|  _ \    / \  |  \/  |
    {COR_CIANO}  | | |  _| | |  |  _|| |  _| |_) |  / _ \ | |\/| |
    {COR_CIANO}  | | | |___| |__| |__| |_| |  _ <  / ___ \| |  | |
    {COR_CIANO}  |_| |_____|_____|_____\____|_| \_\/_/   \_\_|  |_|

    {COR_RESET}   >>> Server Online • Debian 32-bit • v3.0  By Celso Jr. & Telegram FZ-LLC <<<
    """
    print(logo)
    print(f"Comandos: {COR_AMARELO}chat [nome]{COR_RESET} para escolher amigo | {COR_AMARELO}listar{COR_RESET} para ver contatos.")
    print(f"          {COR_AMARELO}upload [arquivo]{COR_RESET} para enviar | {COR_AMARELO}sair{COR_RESET} para fechar.\n")

def obter_nome(user_id, first_name="Desconhecido"):
    if user_id in AMIGOS:
        return f"{COR_ROSA}{AMIGOS[user_id]}{COR_RESET}"
    return f"{first_name} (ID: {user_id})"

# --- RECEBER MENSAGENS (Background) ---
@bot.message_handler(func=lambda m: True)
def receber_texto(message):
    nome = obter_nome(message.chat.id, message.from_user.first_name)
    print(f"\n\r{COR_CIANO}[{nome}]:{COR_RESET} {message.text}")
    print(f"\r{COR_VERDE}Você ({chat_atual_nome}) > {COR_RESET}", end="", flush=True)

@bot.message_handler(content_types=['document', 'photo', 'audio', 'video'])
def receber_arquivo(message):
    nome_user = obter_nome(message.chat.id, message.from_user.first_name)
    try:
        if message.content_type == 'document':
            fid = message.document.file_id; fname = message.document.file_name
        elif message.content_type == 'photo':
            fid = message.photo[-1].file_id; fname = f"foto_{fid[-5:]}.jpg"
        else:
            fid = getattr(message, message.content_type).file_id; fname = f"{message.content_type}_{fid[-5:]}"

        path = bot.get_file(fid).file_path
        downloaded = bot.download_file(path)
        with open(fname, 'wb') as f: f.write(downloaded)

        print(f"\n\r{COR_AMARELO}[ARQUIVO DE {nome_user}]: {fname} salvo!{COR_RESET}")
        bot.reply_to(message, f"✅ Recebi: {fname}")
        print(f"\r{COR_VERDE}Você ({chat_atual_nome}) > {COR_RESET}", end="", flush=True)
    except Exception as e: print(f"\nErro download: {e}")

# --- LOOP PRINCIPAL DO TERMINAL ---
def loop_terminal():
    global chat_atual_id, chat_atual_nome
    
    while True:
        try:
            texto = input(f"{COR_VERDE}Você ({chat_atual_nome}) > {COR_RESET}")
            
            if not texto: continue

            # COMANDO: SAIR
            if texto.lower() in ['sair', 'exit']:
                os._exit(0)

            # COMANDO: LISTAR CONTATOS
            elif texto.lower() == 'listar':
                print(f"\n{COR_AMARELO}--- SEUS CONTATOS ---{COR_RESET}")
                for id_num, nome in AMIGOS.items():
                    print(f"- {nome} (ID: {id_num})")
                print("-" * 20)

            # COMANDO: CHAT (Mudar de conversa)
            elif texto.lower().startswith("chat "):
                busca = texto.split(" ", 1)[1].lower()
                encontrou = False
                
                # Procura no dicionário AMIGOS
                for id_num, nome_amigo in AMIGOS.items():
                    if busca in nome_amigo.lower():
                        chat_atual_id = id_num
                        chat_atual_nome = nome_amigo
                        print(f"{COR_ROSA}>>> Conversando agora com: {chat_atual_nome} <<<{COR_RESET}")
                        encontrou = True
                        break
                
                if not encontrou:
                    # Tenta ver se a pessoa digitou o ID direto (números)
                    if busca.isdigit():
                        chat_atual_id = int(busca)
                        chat_atual_nome = f"ID {busca}"
                        print(f"{COR_ROSA}>>> ID Manual definido: {busca} <<<{COR_RESET}")
                    else:
                        print(f"❌ Amigo '{busca}' não encontrado na lista AMIGOS.")

            # COMANDO: UPLOAD
            elif texto.lower().startswith("upload "):
                if not chat_atual_id:
                    print("❌ Selecione um amigo primeiro! Use: chat [nome]")
                    continue
                arquivo = texto.split(" ", 1)[1]
                if os.path.exists(arquivo):
                    print(f"Enviando {arquivo} para {chat_atual_nome}...")
                    with open(arquivo, 'rb') as d: bot.send_document(chat_atual_id, d)
                else: print("❌ Arquivo não existe.")

            # MENSAGEM NORMAL (Envia para o chat atual)
            else:
                if chat_atual_id:
                    bot.send_message(chat_atual_id, texto)
                else:
                    print("⚠️ Ninguém selecionado. Digite 'chat [nome]' ou espere alguém mandar Oi.")

        except Exception as e:
            print(f"Erro: {e}")

# Start
mostrar_banner()
t = threading.Thread(target=bot.infinity_polling); t.daemon = True; t.start()
loop_terminal()
