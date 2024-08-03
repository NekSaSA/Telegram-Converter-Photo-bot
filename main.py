import asyncio
import logging
from io import BytesIO
from os import remove

from skimage import io as sk_io
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder

API_TOKEN = '7299165407:AAEmfJBwwT7zIwH-cAbRvXOPHkx-3sGyeWw'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

SUPPORTED_FORMATS = ['jpg', 'jpeg', 'png', 'webp', 'bmp', 'ppm']
file_storage = {}
format_storage = {}

@dp.message(CommandStart())
async def send_welcome(message: Message):
    await message.answer('Hello, please send me an image and I will be happy to convert it for you!')

@dp.message(F.photo)
async def handle_image(message: Message):
    file_id = message.photo[-1].file_id
    message_id = message.message_id
    file_storage[message_id] = file_id

    keyboard = InlineKeyboardBuilder()
    for fmt in SUPPORTED_FORMATS:
        keyboard.add(InlineKeyboardButton(text=fmt, callback_data=f"{fmt}:{message_id}"))
    keyboard.adjust(2)

    await message.answer('Please select the image format you would like to convert:', reply_markup=keyboard.as_markup())

@dp.callback_query(F.data)
async def process_callback(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    format_to_convert, message_id_str = callback_query.data.split(':')
    message_id = int(message_id_str)
    file_id = file_storage.get(message_id)

    if file_id:
        if format_storage.get(message_id) == format_to_convert:
            await callback_query.message.answer(f'Image is already converted to {format_to_convert}.')
            return

        try:
            file_info = await bot.get_file(file_id)
            file = await bot.download_file(file_info.file_path)

            img = sk_io.imread(BytesIO(file.read()))
            output_path = f'{message_id}.{format_to_convert}'

            sk_io.imsave(output_path, img)

            input_file = FSInputFile(output_path)
            await bot.send_document(callback_query.from_user.id, input_file)

            # Cleanup
            remove(output_path)
            format_storage[message_id] = format_to_convert  # Store the format

            await callback_query.message.answer(f'Image converted to {format_to_convert} and sent successfully!')
        except Exception as e:
            logging.error(f"Error processing file: {e}")
            await callback_query.message.answer('An error occurred while processing the image. Please try again.')
    else:
        await callback_query.message.answer('Image not found. Please resend the image and try again.')

async def on_shutdown(dp: Dispatcher):
    await bot.session.close()

async def main():
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await on_shutdown(dp)

if __name__ == '__main__':
    asyncio.run(main())
