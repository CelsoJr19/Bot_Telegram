import telebot
import os

# --- CONFIGURAÇÃO ---
# Cole seu Token do BotFather aqui
TOKEN = "8481778524:AAG3hsguneuoMwMnAbnsLoo-c7RzTtU-QRk"

# Coloque o SEU ID do Telegram aqui para segurança (opcional, mas recomendado)
# Para descobrir seu ID, mande mensagem para o @userinfobot no Telegram
SEU_ID = 0  # Troque 0 pelo número do seu ID se quiser restringir acesso

bot = telebot.TeleBot(TOKEN)

print("--- Bot do Notebook Iniciado ---")

# Função para verificar se é você falando (Segurança básica)
def eh_o_dono(message):
    if SEU_ID == 0: return True # Se for 0, aceita todo mundo (cuidado!)
    return message.from_user.id == SEU_ID

# 1. Comando /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    if not eh_o_dono(message): return
    bot.reply_to(message, "Olá! Sou seu Notebook Debian.\n\n"
                          "Comandos:\n"
                          "/listar - Ver arquivos na pasta\n"
                          "/baixar [nome] - Baixar arquivo\n"
                          "Ou me envie um arquivo para eu salvar.")

# 2. Comando /listar (Mostra arquivos da pasta atual)
@bot.message_handler(commands=['listar'])
def listar_arquivos(message):
    if not eh_o_dono(message): return
    arquivos = os.listdir('.') # Lista pasta atual
    arquivos_str = "\n".join(arquivos)
    if not arquivos:
        bot.reply_to(message, "Pasta vazia.")
    else:
        bot.reply_to(message, f"📂 Arquivos no Notebook:\n\n{arquivos_str}")

# 3. Comando /baixar (Envia arquivo do Notebook pro Celular)
@bot.message_handler(commands=['baixar'])
def baixar_arquivo(message):
    if not eh_o_dono(message): return
    try:
        # Pega o nome do arquivo depois do comando
        nome_arquivo = message.text.split(" ", 1)[1]
        if os.path.exists(nome_arquivo):
            bot.reply_to(message, f"Enviando {nome_arquivo}...")
            with open(nome_arquivo, 'rb') as doc:
                bot.send_document(message.chat.id, doc)
        else:
            bot.reply_to(message, "Arquivo não encontrado!")
    except IndexError:
        bot.reply_to(message, "Use: /baixar nome_do_arquivo")

# 4. Receber Arquivos (Salva do Celular pro Notebook)
@bot.message_handler(content_types=['document', 'photo'])
def salvar_arquivo(message):
    if not eh_o_dono(message): return
    try:
        if message.content_type == 'document':
            file_info = bot.get_file(message.document.file_id)
            nome_original = message.document.file_name
        elif message.content_type == 'photo':
            # Pega a foto de maior qualidade
            file_info = bot.get_file(message.photo[-1].file_id)
            nome_original = f"foto_{message.photo[-1].file_id}.jpg"

        downloaded_file = bot.download_file(file_info.file_path)

        with open(nome_original, 'wb') as new_file:
            new_file.write(downloaded_file)

        bot.reply_to(message, f"✅ Arquivo '{nome_original}' salvo no Debian!")
        print(f"Arquivo recebido: {nome_original}")
        
    except Exception as e:
        bot.reply_to(message, f"Erro ao salvar: {e}")

# Mantém o bot rodando
bot.infinity_polling()
