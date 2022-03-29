import os

from telebot import TeleBot
from dotenv import load_dotenv

from backend.models import Post, BotUser

env_path = os.path.join(os.path.dirname(
    os.path.dirname(os.path.dirname(__file__))), '.env')
load_dotenv(env_path)


TOKEN = os.getenv('TOKEN')


def send_post(post_id: int):
    post = Post.posts.get(id=post_id)
    bot = TeleBot(token=TOKEN, parse_mode='HTML')
    for user in BotUser.users.all():
        try:
            if post.image:
                with open(post.image, 'rb') as file:
                    data = file.read()
                bot.send_photo(user.chat_id, data, post.gettext())
            else:
                bot.send_message(user.chat_id, post.gettext())
        except Exception:
            continue
