import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import CommandStart
from config import *
from keyboards.reply_kb import *
dp = Dispatcher()
bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
from manager_utils import *
from user_utils import *
@dp.message(CommandStart())
async def command_start(message: Message):
    await message.answer(f"Здравствуйте, <b>{message.from_user.full_name}</b>!\nВы запустили бота по поиску вакансий! Желаем удачи в поиске работы.\n",
                         reply_markup=kb_register)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

