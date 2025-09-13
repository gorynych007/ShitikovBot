import json
import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message, ReplyKeyboardMarkup, KeyboardButton, FSInputFile,
    InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
)
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Router
from aiogram.client.default import DefaultBotProperties

# 🔧 Настройки через .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
PHOTO_PATH = "welcome.jpeg"
USERS_FILE = "users.json"
VIDEO_URL = "https://rutube.ru/video/private/c947126ff41010ec1569c1cf15ebccb5/?p=lQ0V4DT8ANAYpue_xNDdVQ"

dp = Dispatcher(storage=MemoryStorage())
router = Router()
dp.include_router(router)

# Фотки к постам
PHOTOS = {
    "p1": "p1.jpeg",
    "p2": "p2.jpeg",
    "p3": "p3.jpeg",
    "p4": "p4.jpeg",
    "p5": "p5.jpeg",
    "p6": "p6.jpeg",
    "p7": "p7.jpeg",
}

# 📁 Работа с пользователями
def load_users():
    if Path(USERS_FILE).exists():
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_users(users_dict):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users_dict, f, ensure_ascii=False, indent=2)


users = load_users()

# 📲 Кнопки
def get_contact_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📱 Поделиться контактом", request_contact=True)]],
        resize_keyboard=True
    )


def get_restart_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🔄 Перезапустить бота")]],
        resize_keyboard=True
    )


def get_watch_video_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📹 Посмотреть видео", url=VIDEO_URL)],
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
    "Нажимай «📱 Поделиться контактом», чтобы отправить контакт.\n\n"
    "Если кнопки нет — нажми на иконку в правом углу)"
)

VIDEO_TEXT = (
    "Очень рад видеть тебя здесь и благодарю за доверие. "
    "В этом видеоуроке я подробно показываю, как можно "
    "<b>выйти на доход от 100.000 рублей в месяц на дизайне инфографики.</b>\n\n"
    "Этот урок — реальный путь, через который прошел я и мои ученики. "
    "Это настоящая карта, которая шаг за шагом приведёт тебя к результату.\n\n"
    "Прошу только об одном — не откладывай просмотр. «Потом» легко превращается в «никогда». "
    "Лучше начни прямо сейчас — урок уже отправлен тебе в боте ниже.\n\n"
    "Приятного просмотра!"
)

# 📸 Отправка фото с текстом
async def send_photo_with_text(bot: Bot, user_id: int, photo_path: str, caption: str, reply_markup=None):
    photo = FSInputFile(photo_path)
    await bot.send_photo(chat_id=user_id, photo=photo, caption=caption, reply_markup=reply_markup, parse_mode=ParseMode.HTML)

# 🚨 Напоминания
async def reminder_task(bot: Bot, user_id: int, username: str):
    uid = str(user_id)

    # Через 3 часа
    await asyncio.sleep(3 * 60 * 60)
    if not users.get(uid, {}).get("contact", False):
        text = (
            f"{username}, ты тут?\nМне реально нужно тебе кое-что важное сказать…\n\n"
            "Представь, что у тебя уже есть в руках рабочий план, который может "
            "<b>вывести тебя на доход от 100.000 рублей в месяц с инфографики.</b>\n"
            "Не сухая теория, не красивые обещания, а конкретные шаги, которые я расписал для тебя в видео.\n\n"
            "Без воды, без догадок, без этих бесконечных «а вдруг не получится».\n"
            "Ты просто включаешь видео, смотришь <b>всего 20 минут</b> и выписываешь для себя первые шаги.\n"
            "И это может стать тем моментом, после которого твой доход реально начнёт расти.\n\n"
            "Каждый день промедления = потерянные клиенты и деньги, которые могли быть у тебя на карте.\n"
            "Серьезно, всего 20 минут, а отдача может быть на годы вперёд.\n\n"
            "<b>Так что включай видео прямо сейчас и начинай строить систему, которая работает на тебя.</b>"
        )
        await send_photo_with_text(bot, user_id, PHOTOS["p1"], text, get_contact_keyboard())

    # Через 6 часов
    await asyncio.sleep(3 * 60 * 60)
    if not users.get(uid, {}).get("contact", False):
        text = (
            "Смотри, тут всё просто.\n"
            "Есть два типа людей:\n"
            "1. Те, кто читают посты, кивают «о, классная идея» и ничего не делают.\n"
            "2. Те, кто берут готовый инструмент и используют его.\n\n"
            "Я сделал для тебя инструмент — видео с пошаговым планом "
            "<b>выхода на 100.000₽ в месяц на инфографике.</b>\n"
            "<b>20 минут времени</b> — и у тебя есть карта действий.\n\n"
            "Вопрос: в какой категории хочешь остаться ты?\n\n"
            "Подтверждай, что ты человек — и я дам тебе доступ к видео."
        )
        await send_photo_with_text(bot, user_id, PHOTOS["p7"], text, get_contact_keyboard())

    # Через 9 часов
    await asyncio.sleep(3 * 60 * 60)
    if not users.get(uid, {}).get("contact", False):
        text = (
            "Ну ладно, надеюсь ты не бот)\n\n"
            "Держи гайд, обязательно досматривай до конца и забирай подарок, "
            "он тебе поможет быстрее выстроить поток клиентов и выйти на желанный доход."
        )
        await send_photo_with_text(bot, user_id, PHOTOS["p2"], text, get_watch_video_keyboard())

    # Через 3 часа после контакта
    await asyncio.sleep(3 * 60 * 60)
    if users.get(uid, {}).get("contact", False) and not users[uid].get("watched", False):
        text = (
            f"{username}, ты тут?\nМне реально нужно тебе кое-что важное сказать…\n\n"
            "Представь, что у тебя уже есть в руках рабочий план, который может "
            "<b>вывести тебя на доход от 100.000 рублей в месяц с инфографики.</b>\n"
            "Не сухая теория, не красивые обещания, а конкретные шаги, которые я расписал для тебя в видео.\n\n"
            "Без воды, без догадок, без этих бесконечных «а вдруг не получится».\n"
            "Ты просто включаешь видео, смотришь <b>всего 20 минут</b> и выписываешь для себя первые шаги.\n"
            "И это может стать тем моментом, после которого твой доход реально начнёт расти.\n\n"
            "Каждый день промедления = потерянные клиенты и деньги, которые могли быть у тебя на карте.\n"
            "Серьезно, всего 20 минут, а отдача может быть на годы вперёд.\n\n"
            "<b>Так что включай видео прямо сейчас и начинай строить систему, которая работает на тебя.</b>"
        )
        await send_photo_with_text(bot, user_id, PHOTOS["p3"], text, get_watch_video_keyboard())

    # Через 9 часов
    await asyncio.sleep(6 * 60 * 60)
    if not users[uid].get("watched", False):
        text = (
            "Представь: проходит всего месяц.\n"
            "Ты открываешь кошелёк и видишь там не мелкие остатки после дешёвых заказов, "
            "а <b>стабильные 100.000 рублей</b>, которые приходят тебе за инфографику.\n\n"
            "Ты больше не тратишь время на бесконечные поиски клиентов, не гадаешь, «а что вообще делать», "
            "не переживаешь, что твой труд стоит копейки.\n\n"
            "У тебя есть ясная система: шаг за шагом ты знаешь, что делать, как привлекать клиентов, "
            "как показывать свою ценность, и самое главное — как зарабатывать стабильно.\n\n"
            "И вот что самое важное: этот путь у тебя уже есть в руках.\n"
            "Я упаковал его в короткое видео, где показал пошаговый план, как выйти на 100.000 рублей с инфографики.\n"
            "Всего 20 минут — и ты получаешь готовую карту.\n\n"
            "Ты можешь тянуть и откладывать. Но каждый день промедления — это деньги, которые могли бы быть у тебя уже завтра.\n"
            "Серьезно, подумай: <b>пока ты думаешь «ну потом», твои клиенты уходят к другим.</b>\n\n"
            "<b>Хочешь изменений? Тогда не жди.</b>\n"
            "Смотри видео прямо сейчас и начинай строить себе доход, который будет работать на тебя."
        )
        await send_photo_with_text(bot, user_id, PHOTOS["p4"], text, get_watch_video_keyboard())

    # Через 12 часов
    await asyncio.sleep(11 * 60 * 60)
    if not users[uid].get("watched", False):
        text = (
            "<b>Знаешь, что самое опасное?</b>\n"
            "Не то, что ты чего-то не знаешь. И даже не то, что конкуренция большая.\n"
            "Самое опасное — это откладывание.\n\n"
            "Потому что каждый день, <b>пока ты думаешь «ну потом», твои клиенты уходят к другим.</b>\n"
            "А вместе с ними уходят и деньги.\n\n"
            "А у тебя уже есть то, что способно это изменить.\n"
            "Видео, где я собрал пошаговый план, как выйти на доход от 100.000 рублей в месяц с инфографики.\n"
            "Это не теория, не пустые обещания.\nЭто конкретные шаги, которые работают.\n\n"
            "<b>Всего 20 минут — и ты понимаешь, как перестать терять и начать зарабатывать.</b>\n\n"
            "Реши для себя честно:\nты хочешь продолжать наблюдать, как мимо проходят твои деньги?\n"
            "<b>Если второе — смотри видео прямо сегодня.</b>\n"
            "Это может стать точкой, после которой твоя жизнь реально поменяется."
        )
        await send_photo_with_text(bot, user_id, PHOTOS["p5"], text, get_watch_video_keyboard())

    # Через 24 часа
    await asyncio.sleep(23 * 60 * 60)
    if not users[uid].get("watched", False):
        text = (
            "Сейчас ты можешь продолжать брать заказы за копейки, переживать из-за конкурентов и гадать, "
            "«получится ли вообще заработать нормально».\n\n"
            "<b>А можешь за 20 минут посмотреть видео, где я показал пошаговый план выхода на 100.000 рублей с инфографики.</b>\n\n"
            "И это не пустые слова.\nОдин мой ученик сделал ровно так.\n"
            "Он был в той же ситуации, что и ты: не знал, как закрывать клиентов, сомневался, что у него получится, и брал заказы за минимальные суммы.\n"
            "Потом обратился ко мне…\n\n"
            "Что вышло?\n<b>За 2 месяца работы его доход превысил 300.000 рублей.</b>\n\n"
            "Представь: всего пара недель внедрения — и жизнь меняется полностью. И самое главное — его путь, максимально похож на тот план, который я даю тебе в видео."
        )
        await send_photo_with_text(bot, user_id, PHOTOS["p6"], text, get_watch_video_keyboard())

    # Через 48 часов
    await asyncio.sleep(48 * 60 * 60)
    if not users[uid].get("watched", False):
        text = (
            "<b>Как я нашёл клиента на 120.000₽ всего за неделю рассылок?</b>\n\n"
            "История простая.\nВ моменте понимаю, что клиентов стало у меня меньше, стал слишком много времени уделять другим аспектам жизни.\n"
            "Значит сейчас нужно минимум времени на поиск клиентов, поэтому необходимо найти одного и крупного.\n\n"
            "Не долго думая, начинаю просто штурмовать лички в озоне по своей системе, с проверенными офферами.\n\n"
            "И что ты думаешь?\nЧерез пару дней и один созвон у меня на руках договор на 120.000₽.\n\n"
            "К чему эта история?\nЧтобы показать: деньги реально рядом.\n\n"
            "<b>Посмотри видео, где я собрал пошаговый план, как выйти на доход от 100.000 рублей с инфографики.</b>\n"
            "20 минут просмотра могут реально стать твоим переломным моментом."
        )
        await send_photo_with_text(bot, user_id, PHOTOS["p6"], text, get_watch_video_keyboard())

# ▶️ Старт / Перезапуск
@router.message(F.text == "/start")
@router.message(F.text == "🔄 Перезапустить бота")
async def start_handler(message: Message):
    uid = str(message.from_user.id)
    users.setdefault(uid, {"contact": False, "watched": False,
                           "username": message.from_user.username or message.from_user.first_name})
    save_users(users)

    photo = FSInputFile(PHOTO_PATH)
    await message.answer_photo(
        photo=photo,
        caption=WELCOME_TEXT,
        reply_markup=get_contact_keyboard()
    )
    asyncio.create_task(reminder_task(message.bot, message.from_user.id, users[uid]["username"]))

# 📩 Обработка контакта
@router.message(F.contact)
async def contact_handler(message: Message, bot: Bot):
    uid = str(message.from_user.id)
    contact = message.contact
    users[uid]["contact"] = True
    save_users(users)

    text = (
        f"📞 Новый контакт\n"
        f"ID: {message.from_user.id}\n"
        f"User: @{message.from_user.username or 'без username'}\n"
        f"Имя: {contact.first_name} {contact.last_name or ''}\n"
        f"Номер: {contact.phone_number}"
    )
    await bot.send_message(chat_id=ADMIN_ID, text=text)

    await message.answer("Контакт получен ✅", reply_markup=get_restart_keyboard())
    await message.answer(VIDEO_TEXT, reply_markup=get_watch_video_keyboard())

# ✅ Обработка нажатия «Посмотрел видео»
@router.callback_query(F.data == "watched_video")
async def watched_video_handler(call: CallbackQuery):
    uid = str(call.from_user.id)
    users[uid]["watched"] = True
    save_users(users)

    await call.answer("Отлично! Продолжай в том же духе! 🔥")
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer(
        "Спасибо за просмотр, не забывай написать мне и воспользоваться подарком)\n\nУже жду сообщение от тебя!",
        reply_markup=get_message_me_keyboard()
    )

# 📬 Админ команды
@router.message(F.from_user.id == ADMIN_ID, F.text)
async def admin_handler(message: Message, bot: Bot):
    if message.text.startswith("/status "):
        parts = message.text.split(maxsplit=1)
        uid = parts[1]
        if uid in users:
            await message.answer(
                f"Пользователь {uid} статус:\nКонтакт: {users[uid]['contact']}\nВидео: {users[uid]['watched']}")
        else:
            await message.answer("Пользователь не найден.")
    elif message.text == "/users":
        await message.answer("Пользователи:\n" + "\n".join(users.keys()))
    elif message.text.startswith("/send "):
        try:
            parts = message.text.split(maxsplit=2)
            user_id = int(parts[1])
            text = parts[2]
            await bot.send_message(chat_id=user_id, text=text)
            await message.answer(f"✅ Сообщение отправлено пользователю {user_id}")
        except Exception as e:
            await message.answer(f"❌ Ошибка: {e}")
    else:
        # массовая рассылка
        for uid in users:
            if int(uid) == ADMIN_ID:
                continue
            try:
                await bot.send_message(chat_id=int(uid), text=message.text)
            except Exception as e:
                print(f"Не удалось отправить сообщение {uid}: {e}")

# 🚀 Запуск
async def main():
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
