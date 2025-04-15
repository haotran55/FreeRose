import telebot
from telebot import types
import json
import os
TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
warnings = {}  # user warnings
filters = {}   # filtered keywords
welcomes = {}  # welcome messages
rules = {}     # rules per group

def save_data():
    with open('data.json', 'w') as f:
        json.dump({'warnings': warnings, 'filters': filters, 'welcomes': welcomes, 'rules': rules}, f)

def load_data():
    global warnings, filters, welcomes, rules
    if os.path.exists('data.json'):
        with open('data.json', 'r') as f:
            data = json.load(f)
            warnings = data.get('warnings', {})
            filters = data.get('filters', {})
            welcomes = data.get('welcomes', {})
            rules = data.get('rules', {})

load_data()

def is_admin(message):
    try:
        member = bot.get_chat_member(message.chat.id, message.from_user.id)
        return member.status in ['administrator', 'creator']
    except:
        return False

# Ban command
@bot.message_handler(commands=['ban'])
def ban_user(message):
    if not is_admin(message): return
    if message.reply_to_message:
        try:
            bot.kick_chat_member(message.chat.id, message.reply_to_message.from_user.id)
            bot.reply_to(message, "Đã ban người dùng.")
        except Exception as e:
            bot.reply_to(message, f"Lỗi: {e}")

# Kick command
@bot.message_handler(commands=['kick'])
def kick_user(message):
    if not is_admin(message): return
    if message.reply_to_message:
        try:
            user_id = message.reply_to_message.from_user.id
            bot.kick_chat_member(message.chat.id, user_id)
            bot.unban_chat_member(message.chat.id, user_id)
            bot.reply_to(message, "Đã kick người dùng.")
        except Exception as e:
            bot.reply_to(message, f"Lỗi: {e}")

# Mute command
@bot.message_handler(commands=['mute'])
def mute_user(message):
    if not is_admin(message): return
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        bot.restrict_chat_member(message.chat.id, user_id, can_send_messages=False)
        bot.reply_to(message, "Đã mute người dùng.")

# Unmute
@bot.message_handler(commands=['unmute'])
def unmute_user(message):
    if not is_admin(message): return
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        bot.restrict_chat_member(message.chat.id, user_id, can_send_messages=True)
        bot.reply_to(message, "Đã unmute người dùng.")

# Warn system
@bot.message_handler(commands=['warn'])
def warn_user(message):
    if not is_admin(message): return
    if message.reply_to_message:
        key = f"{message.chat.id}:{message.reply_to_message.from_user.id}"
        warnings[key] = warnings.get(key, 0) + 1
        if warnings[key] >= 3:
            try:
                bot.kick_chat_member(message.chat.id, message.reply_to_message.from_user.id)
                bot.reply_to(message, "Người dùng bị ban vì nhận 3 cảnh cáo.")
                del warnings[key]
            except Exception as e:
                bot.reply_to(message, f"Lỗi: {e}")
        else:
            bot.reply_to(message, f"Đã cảnh cáo người dùng. Tổng: {warnings[key]}")
    save_data()

# Filter system
@bot.message_handler(commands=['filter'])
def add_filter(message):
    if not is_admin(message): return
    args = message.text.split(maxsplit=1)
    if len(args) < 2: return
    word = args[1].lower()
    filters.setdefault(str(message.chat.id), []).append(word)
    bot.reply_to(message, f"Đã thêm từ khóa `{word}` vào bộ lọc.", parse_mode='Markdown')
    save_data()

@bot.message_handler(commands=['stop'])
def remove_filter(message):
    if not is_admin(message): return
    args = message.text.split(maxsplit=1)
    if len(args) < 2: return
    word = args[1].lower()
    try:
        filters[str(message.chat.id)].remove(word)
        bot.reply_to(message, f"Đã xóa từ khóa `{word}` khỏi bộ lọc.", parse_mode='Markdown')
        save_data()
    except:
        bot.reply_to(message, "Không tìm thấy từ khóa trong bộ lọc.")

# Welcome system
@bot.message_handler(commands=['setwelcome'])
def set_welcome(message):
    if not is_admin(message): return
    args = message.text.split(maxsplit=1)
    if len(args) < 2: return
    welcomes[str(message.chat.id)] = args[1]
    bot.reply_to(message, "Đã cập nhật tin nhắn chào mừng.")
    save_data()

@bot.message_handler(commands=['setrules'])
def set_rules(message):
    if not is_admin(message): return
    args = message.text.split(maxsplit=1)
    if len(args) < 2: return
    rules[str(message.chat.id)] = args[1]
    bot.reply_to(message, "Đã cập nhật nội quy.")
    save_data()

@bot.message_handler(commands=['rules'])
def send_rules(message):
    rule = rules.get(str(message.chat.id), "Chưa có nội quy.")
    bot.reply_to(message, rule)

# Welcome new members
@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_user(message):
    text = welcomes.get(str(message.chat.id), None)
    if text:
        for user in message.new_chat_members:
            bot.send_message(message.chat.id, text.replace('{name}', user.first_name))

# Auto delete messages with filtered words
@bot.message_handler(func=lambda m: True, content_types=['text'])
def check_filter(message):
    wordlist = filters.get(str(message.chat.id), [])
    for word in wordlist:
        if word in message.text.lower():
            try:
                bot.delete_message(message.chat.id, message.message_id)
                return
            except:
                pass

# Start command
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Bot quản lý nhóm Rose đã sẵn sàng!")

if __name__ == "__main__":
    print("Bot đang chạy...")
    bot.polling()
