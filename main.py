import asyncio
import datetime

import logging

import easyocr

from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.strategy import FSMStrategy
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder




bot = Bot(token="")
dp = Dispatcher(fsm_strategy=FSMStrategy.GLOBAL_USER)

logging.basicConfig(level=logging.INFO)


async def scheduled(wait_for):
    while True:
        now = datetime.datetime.now().time()
        await asyncio.sleep(wait_for)
        if now.minute == 40 and now.hour == 9 and now.second == 1:
            pass

@dp.message(F.text == "/chatid")
async def chatid(message: types.Message, state: FSMContext):
    await message.answer(str(message.chat.id))

@dp.message(F.text == "/users_file")
async def users_file(message: types.Message):
    await message.answer_document(FSInputFile('users.txt'))


@dp.message(F.text == "/start")
async def send_welcome(message: types.Message, state: FSMContext):

    print('start')
    f = open('users.txt')
    if message.from_user.username and message.from_user.username in f.read():
        f.close()
    elif message.from_user.username:
        f.close()
        f = open('users.txt', 'a')
        f.write(message.from_user.username + '\n')
        f.close()
    await message.answer('Пришлите мне изображение и я распознаю текст на нем!')





@dp.message(F.photo)
async def rb(message: Message, state: FSMContext):
    m = await message.answer('Идет обработка...')

    await bot.download(message.photo[-1], 'photo.png')
    reader = easyocr.Reader(['en', 'ru'])
    result = reader.readtext('photo.png', detail=0)
    result = ' '.join(result)
    await m.edit_text(f'Текст из картинки:\n\n{result}')



async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(scheduled(1))
    try:
        loop.run_until_complete(dp.start_polling(bot))
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()
