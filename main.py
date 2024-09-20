import os
import time
import google.generativeai as genai
# from google.generativeai import GenerateTextRequest, client_options
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters

genai.configure(api_key=os.getenv("API_KEY_GENAI"))
# Crear una instancia del modelo a utilizar
_model = genai.GenerativeModel("gemini-1.5-flash")

#crear una instancia del estado de la conversación
conversation_state = {}
MAX_HISTORY_LENGTH = 10

def save_conversation_state(user_id, text, response):
    if user_id not in conversation_state:
        conversation_state[user_id] = []
    conversation_state[user_id].append({
        "timestamp": time.time(),
        "text": text,
        "response": response
    })
    # Limitar el historial
    if len(conversation_state[user_id]) > MAX_HISTORY_LENGTH:
        conversation_state[user_id].pop(0)

def generate_text(prompt):
    try:
        response = _model.generate_content(prompt)
        print(f"modal: {_model}")
        return response.text
    except Exception as e:
        print(f"Error al generar texto: {e}")
        return "Lo siento, hubo un error al procesar tu solicitud."

# Función para generar texto a partir de una pregunta
def generate(text ="", user_id = 0):
    user_id = user_id
    response = generate_text(text)

    save_conversation_state(user_id, text, response)

    return response

#  Función que se ejecutará cuando alguien envíe un mensaje
def echo(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    user_id = update.effective_user.id
    message = generate(text, user_id)
    update.message.reply_text(message)

# Función que se ejecutará cuando alguien use el comando /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'¡Hola! @{user.username}, Soy tu bot de prueba. ¿Cómo puedo ayudarte?')
    # update.message.reply_text(f'@{user.username}, Que chucha quieres, ya estoy trabajando, no me jodas >:v')

# Función para manejar el comando /help
def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Aquí están los comandos disponibles:\n/start - Iniciar el bot\n/help - Obtener ayuda sobre los comandos disponibles \n/generate - Generar texto a partir de una pregunta\n/config para configuracion del bot \n/print_state para ver el estado de la conversación')

def config_command(update: Update, context: CallbackContext) -> None:
    split_message = update.message.text.split("/config ")
    if len(split_message) < 2:
        update.message.reply_text('Aqui puedes realizar diferentes configuraciones, si deceas cambiar el modelo de IA, escribe /config model=gemini-1.5-flash')
        return
    message = split_message[1].lower()
    if "model=" in message:
        new_model = message.split("model=")[1]
        _model = genai.GenerativeModel(new_model)
        update.message.reply_text('Modelo cambiado a ' + new_model)

def print_state_command(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    if user_id in conversation_state:
        update.message.reply_text(conversation_state[user_id])
    else:
        update.message.reply_text("No hay mensajes anteriores")

def main():
    # Obtenemos el token desde la variable de entorno TELEGRAM_TOKEN
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        print("Error: No se encontró el token de Telegram en la variable de entorno.")
        return

    updater = Updater(token, use_context=True)

    # Obtiene el dispatcher para registrar los manejadores de comandos
    dispatcher = updater.dispatcher

    # Registro de comandos
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    # dispatcher.add_handler(CommandHandler("generate", generate_command))
    dispatcher.add_handler(CommandHandler("print_state", print_state_command))
    dispatcher.add_handler(CommandHandler("config", config_command))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))


    # Inicia el bot
    updater.start_polling()

    # Mantiene el bot corriendo hasta que se detenga
    updater.idle()

if __name__ == '__main__':
    main()
