import asyncio
import logging
from datetime import datetime
from telethon import TelegramClient, events
from telethon.tl.types import User
import anthropic

API_ID = 37110545
API_HASH = ‘8653918a5c9f2f34d2ccb681df85f648’
ANTHROPIC_API_KEY = ‘вставьте_ваш_ключ_сюда’
YOUR_NAME = ‘Behzodjon’
AUTO_REPLY_ALL = True
ONLY_PRIVATE = True
REPLY_COOLDOWN_MINUTES = 30

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(**name**)

client = TelegramClient(‘session’, API_ID, API_HASH)
claude = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
replied_users = {}

def should_reply(user_id):
if user_id not in replied_users:
return True
minutes = (datetime.now() - replied_users[user_id]).seconds / 60
return minutes >= REPLY_COOLDOWN_MINUTES

async def generate_reply(message_text, sender_name):
try:
response = claude.messages.create(
model=‘claude-sonnet-4-20250514’,
max_tokens=300,
system=’Ты личный AI ассистент пользователя ’ + YOUR_NAME + ‘. Отвечай от его имени, кратко и вежливо. Отвечай на том же языке что и собеседник.’,
messages=[{‘role’: ‘user’, ‘content’: ’Сообщение от ’ + sender_name + ’: ’ + message_text}]
)
return response.content[0].text
except Exception as e:
logger.error(‘Ошибка: ’ + str(e))
return YOUR_NAME + ’ сейчас занят, свяжется позже.’

@client.on(events.NewMessage(incoming=True))
async def handle_incoming(event):
if ONLY_PRIVATE and not event.is_private:
return
sender = await event.get_sender()
if not isinstance(sender, User) or sender.bot:
return
user_id = sender.id
sender_name = sender.first_name or ‘Незнакомец’
message_text = event.message.text
if not message_text:
return
if not should_reply(user_id):
return
reply = await generate_reply(message_text, sender_name)
await asyncio.sleep(2)
await event.reply(reply)
replied_users[user_id] = datetime.now()

async def main():
await client.start()
me = await client.get_me()
logger.info(‘Автоответчик запущен для @’ + str(me.username))
await client.run_until_disconnected()

if **name** == ‘**main**’:
asyncio.run(main())
