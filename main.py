from token_names import token_tg
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from api_get_file import send_api, send_bot
import io
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text
from aiogram_calendar import simple_cal_callback, SimpleCalendar, dialog_cal_callback, DialogCalendar
from datetime import datetime

bot = Bot(token=token_tg)
dp = Dispatcher(bot)

async def keybord_start():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('За все время')
    button2 = types.KeyboardButton('В определённый день')
    keyboard.add(button1, button2)
    return keyboard

async def keybord_back():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('Назад')
    keyboard.add(button1)
    return keyboard

@dp.message_handler(commands=["start"])
async def start_tg(message: types.Message):
    await message.reply("Выберете вариант статуса о войне", reply_markup=await keybord_start())

# simple calendar usage
@dp.callback_query_handler(simple_cal_callback.filter())
async def process_simple_calendar(callback_query: CallbackQuery, callback_data: dict):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        rend = await send_api(f'/statistics/{date.strftime("%Y-%m-%d")}')
        if rend != 'Вы написали дату в которой не было войны или эта дата в будущем. Напишите пожалуйста другую дату':
            await callback_query.message.answer('Ваша дата принят, ожидайте', reply_markup=await keybord_back())
            await callback_query.message.answer(await send_bot(rend), reply_markup=await keybord_back())
        else:
            await callback_query.message.answer('Вы написали дату, в которой не было войны или эта дата в будущем. Выберете пожалуйста другую дату', reply_markup=await SimpleCalendar().start_calendar())

@dp.message_handler()
async def handle_message(message: types.Message):
    if message.text == "Назад":
        await message.reply("Выберете вариант статуса о войне", reply_markup=await keybord_start())
    elif message.text == "За все время":
        current_date = datetime.now().date()
        formatted_date = current_date.strftime("%Y-%m-%d")
        rend = await send_api(f'/statistics/{formatted_date}')
        await message.reply(await send_bot(rend), reply_markup=await keybord_back())
    elif message.text == "В определённый день":
        await message.reply('Выберете дату', reply_markup=await SimpleCalendar().start_calendar())

if __name__ == "__main__":
    executor.start_polling(dp)