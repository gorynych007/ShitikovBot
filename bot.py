import json
import asyncio
from pathlib import Path

from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message, ReplyKeyboardMarkup, KeyboardButton, FSInputFile,
    InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery,
    ReplyKeyboardRemove
)
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Router
from aiogram.client.default import DefaultBotProperties

# 🔧 Настройки
BOT_TOKEN = "7594750001:AAFrfyRfBZURdIXQwKZbL1ShEEeiEyHbsCk"
ADMIN_ID = 6858116356
PHOTO_PATH = "welcome.jpeg"
USERS_FILE = "users.json"
VIDEO_URL = "https://rutube.ru/video/private/c947126ff41010ec1569c1cf15ebccb5/?p=lQ0V4DT8ANAYpue_xNDdVQ"

dp = Dispatcher(storage=MemoryStorage())
router = Router()
dp.include_router(router)

# 📁 Загрузка пользователей
def load_users():
    if Path(USERS_FILE).exists():
        with open(USERS_FILE, "r") as f:
            return set(json.load(f))
    return set()

def save_users(users_set):
    with open(USERS_FILE, "w") as f:
        json.dump(list(users_set), f)

users = load_users()
confirmed_contacts = set()
watched_video_users = set()

# 📲 Кнопки
def get_contact_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📱 Поделиться", request_contact=True)]],
        resize_keyboard=True
    )

def get_restart_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🔄 Перезапустить бота")]],
        resize_keyboard=True
    )

def get_watch_video_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Посмотреть видео", url=VIDEO_URL)],
        [InlineKeyboardButton(text="Посмотрел видео ✅", callback_data="watched_video")]
    ])

def get_message_me_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Написать мне", url="https://t.me/ArSdesigns")]
    ])

# 📝 Сообщения
WELCOME_TEXT = (
    "Приветствую тебя в своем боте 👋\n\n"
    "Чтобы получить урок, нужно подтвердить, что ты человек.\n\n"
    "Никакого спама, только полезная информация. Будь готов действовать и не стоять на месте.\n\n"
    "Нажимай «📱 Поделиться», чтобы отправить контакт.\n\n"
    "Если нет кнопки — нажми на иконку в правом углу)"
)

VIDEO_TEXT = (
    "Очень рад видеть тебя здесь и благодарю за доверие. "
    "В этом видеоуроке я подробно показываю, как можно выйти на доход от 100.000 рублей в месяц на дизайне инфографики.\n\n"
    "Этот урок — реальный путь, через который прошел я и мои ученики. "
    "Это настоящая карта, которая шаг за шагом приведёт тебя к результату.\n\n"
    "Прошу только об одном — не откладывай просмотр. «Потом» легко превращается в «никогда». "
    "Лучше начни прямо сейчас — урок уже отправлен тебе в боте ниже.\n\n"
    "Приятного просмотра!"
)

# 🚨 Планировщик напоминаний
async def reminder_task(bot: Bot, user_id: int):
    await asyncio.sleep(3 * 60 * 60)
    if user_id not in watched_video_users:
        await bot.send_message(user_id, "Бро, ты тут?", reply_markup=get_restart_keyboard())
    await asyncio.sleep(9 * 60 * 60)
    if user_id not in watched_video_users:
        await bot.send_message(user_id, "Не упусти шанс!", reply_markup=get_restart_keyboard())
    await asyncio.sleep(12 * 60 * 60)
    if user_id not in watched_video_users:
        await bot.send_message(user_id, "Каждый день промедления — минус деньги и опыт", reply_markup=get_restart_keyboard())

# ▶️ Старт / Перезапуск
@router.message(F.text == "/start")
@router.message(F.text == "🔄 Перезапустить бота")
async def start_handler(message: Message):
    users.add(message.from_user.id)
    save_users(users)
    photo = FSInputFile(PHOTO_PATH)
    await message.answer_photo(
        photo=photo,
        caption=WELCOME_TEXT,
        reply_markup=get_contact_keyboard()
    )
    asyncio.create_task(reminder_task(message.bot, message.from_user.id))

# 📩 Обработка контакта
@router.message(F.contact)
async def contact_handler(message: Message, bot: Bot):
    contact = message.contact
    confirmed_contacts.add(message.from_user.id)

    # Отправка админу
    text = (
        f"📞 Новый контакт\n"
        f"ID: {message.from_user.id}\n"
        f"User: @{message.from_user.username or 'без username'}\n"
        f"Имя: {contact.first_name} {contact.last_name or ''}\n"
        f"Номер: {contact.phone_number}"
    )
    await bot.send_message(chat_id=ADMIN_ID, text=text)

    # Убираем ReplyKeyboard
    await message.answer("Контакт получен ✅", reply_markup=get_restart_keyboard())

    # Отправка видео с Inline кнопками
    await message.answer(VIDEO_TEXT, reply_markup=get_watch_video_keyboard())

# ✅ Обработка нажатия «Посмотрел видео»
@router.callback_query(F.data == "watched_video")
async def watched_video_handler(call: CallbackQuery):
    watched_video_users.add(call.from_user.id)
    await call.answer("Отлично! Продолжай в том же духе! 🔥")
    await call.message.edit_reply_markup(reply_markup=None)
    # Отправка сообщения с кнопкой «Написать мне»
    await call.message.answer(
        "Спасибо за просмотр, не забывай написать мне и воспользоваться подарком)\n\nУже жду сообщение от тебя!",
        reply_markup=get_message_me_keyboard()
    )

# 📬 Рассылка от админа
@router.message(F.from_user.id == ADMIN_ID, F.text)
async def admin_handler(message: Message, bot: Bot):
    if message.text.startswith("/send "):
        try:
            parts = message.text.split(maxsplit=2)
            user_id = int(parts[1])
            text = parts[2]
            await bot.send_message(chat_id=user_id, text=text)
            await message.answer(f"✅ Сообщение отправлено пользователю {user_id}")
        except Exception as e:
            await message.answer(f"❌ Ошибка: {e}")
    else:
        for user_id in users:
            if user_id == ADMIN_ID:
                continue
            try:
                await bot.send_message(chat_id=user_id, text=message.text)
            except Exception as e:
                print(f"Не удалось отправить сообщение {user_id}: {e}")

# ▶️ Запуск
async def main():
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
