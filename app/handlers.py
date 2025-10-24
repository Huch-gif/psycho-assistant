python -c
code = '''
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        \"🧠 Привет! Я — ПсихоАссистент.\\n\\n\"
        \"Я здесь, чтобы выслушать тебя, помочь разобраться в чувствах или просто побыть рядом.\\n\\n\"
        \"Напиши мне что-нибудь — я внимательно прочитаю 💬\"
    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    await update.message.reply_text(
        f'Спасибо, что поделился этим: \"{user_text}\".\\n\\n'
        \"Помни: твои чувства важны. Хочешь, поговорим об этом подробнее?\"
    )

def setup_handlers(application):
    application.add_handler(CommandHandler(\"start\", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
'''
with open('app/bot/handlers.py', 'w', encoding='utf-8') as f:
    f.write(code)
print('✅ handlers.py создан в UTF-8')
