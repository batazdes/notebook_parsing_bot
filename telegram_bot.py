from aiogram import Bot, Dispatcher,executor,types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.markdown import hbold,hlink
from config import way_to_directory
from making_url import changing_url
from notebook_parser import citilink_parser
import json
import os
import glob

token = open('token.txt').read()
bot=Bot(token=token, parse_mode=types.ParseMode.HTML)
dp=Dispatcher(bot, storage=MemoryStorage())

available_categories = ['ноутбуки']
pass_keybord = ['пропустить']

url_citilink = 'https://www.citilink.ru/catalog/noutbuki/'
available_manufactures_citilink = ['продолжить','acer','apple','asus','dell','honor','digma','gigabyte','hp','huawei','lenovo']
available_processors_citilink = ['продолжить','athlon gold','athlon silver','ryzen 3','ryzen 5','ryzen 7','ryzen 9','celeron','core i3','core i3','core i5','core i7','core i9']
available_screen_resolution_citilink = ['продолжить','1366х768','1600х900','1920х1080','2560х1600','3024х1964']
available_matrix_type_citilink = ['продолжить','ips','tn','oled']
available_ssd_size_citilink = ['продолжить','128 gb','256 gb','512 gb','1 tb','2 tb']
available_RAM_size_citilink = ['продолжить','4 gb','8 gb','16 gb','32 gb']
available_actions = ['да, вывести','выбрать товары заново']

class ChooseNotebooks(StatesGroup):
    waiting_for_category = State()
    waiting_for_price_min = State()
    waiting_for_price_max = State()
    waiting_for_manufacture = State()
    waiting_for_processors = State()
    waiting_for_screen_resolution = State()
    waiting_for_matrix_type = State()
    waiting_for_ssd_size = State()
    waiting_for_RAM_size = State()
    asking = State()
    parsing = State()

@dp.message_handler(commands="start")
async def start_choosing (message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for category in available_categories:
        keyboard.add(category)
    await message.answer('Какой товар вы бы хотели найти?', reply_markup=keyboard)
    await ChooseNotebooks.waiting_for_category.set()

@dp.message_handler(state=ChooseNotebooks.waiting_for_category)
async def category_choosed (message: types.Message,state: FSMContext):
    if message.text.lower() not in available_categories:
        await message.answer("Пожалуйста, выберете категорию с помощью клавиатуры")
        return
    await state.update_data(chosen_category = message.text.lower())

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(pass_keybord[0])
    await message.answer('Назовите минимальную цену', reply_markup=keyboard)
    await ChooseNotebooks.waiting_for_price_min.set()

@dp.message_handler(state=ChooseNotebooks.waiting_for_price_min)
async def min_price_choosed (message: types.Message,state: FSMContext):
    if message.text.lower() == 'пропустить':
        await state.update_data(chosen_min_price='11090')
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(pass_keybord[0])
        await message.answer('Назовите максимальную цену', reply_markup=keyboard)
        await ChooseNotebooks.waiting_for_price_max.set()

    elif int(message.text) in range (11090,545990):
        await state.update_data(chosen_min_price=message.text)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(pass_keybord[0])
        await message.answer('Назовите максимальную цену', reply_markup=keyboard)
        await ChooseNotebooks.waiting_for_price_max.set()

    else:
        await message.answer("Пожалуйста, ввведите целое число от 11090 до 545990")
        await ChooseNotebooks.waiting_for_price_min.set()

@dp.message_handler(state=ChooseNotebooks.waiting_for_price_max)
async def max_price_choosed (message: types.Message,state: FSMContext):
    user_data = await state.get_data()
    if message.text.lower() == 'пропустить':
        await state.update_data(chosen_max_price='545990')
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for manufacture in available_manufactures_citilink:
            keyboard.add(manufacture)
        await message.answer('Назовите производителя(ей)', reply_markup=keyboard)
        await ChooseNotebooks.waiting_for_manufacture.set()

    elif int(message.text) in range (11090,545990) and int(message.text)>=int(user_data['chosen_min_price']):
        await state.update_data(chosen_max_price=message.text)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for manufacture in available_manufactures_citilink:
            keyboard.add(manufacture)
        await message.answer('Выберете производителя(ей)', reply_markup=keyboard)
        await ChooseNotebooks.waiting_for_manufacture.set()

    else:
        await message.answer("Пожалуйста, ввведите целое число от 11090 до 545990 больше или равное минимальной цене")
        await ChooseNotebooks.waiting_for_price_max.set()

@dp.message_handler(state=ChooseNotebooks.waiting_for_manufacture)
async def manufacture_choosed (message: types.Message,state: FSMContext):
    if message.text.lower() in available_manufactures_citilink:
        if message.text.lower()=='продолжить':
            text = open("data.txt").read()
            await state.update_data(chosen_manufacture=text)
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            with open("data.txt","w") as f:
                f.write("")
            for processor in available_processors_citilink:
                keyboard.add(processor)
            await message.answer('Выберете процессор(ы) для вашего ноутбука',reply_markup=keyboard)
            await ChooseNotebooks.waiting_for_processors.set()
        else:
            with open("data.txt",'a') as f:
                f.write(message.text.lower()+',')
            await message.answer(message.text.lower())
            return
    else:
        await message.answer("Пожалуйста выберете производителя с помощью клавиатуры")
        ChooseNotebooks.waiting_for_manufacture.set()

@dp.message_handler(state=ChooseNotebooks.waiting_for_processors)
async def processor_choosed (message: types.Message,state: FSMContext):
    if message.text.lower() in available_processors_citilink:
        if message.text.lower()=='продолжить':
            text = open("data.txt").read()
            await state.update_data(chosen_processor=text)
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            with open("data.txt","w") as f:
                f.write("")
            for screen_resolution in available_screen_resolution_citilink:
                keyboard.add(screen_resolution)
            await message.answer('Выберете разрешение экрана',reply_markup=keyboard)
            await ChooseNotebooks.waiting_for_screen_resolution.set()
        else:
            with open("data.txt",'a') as f:
                f.write(message.text.lower()+',')
            await message.answer(message.text.lower())
            return
    else:
        await message.answer("Пожалуйста выберете процессор с помощью клавиатуры")
        ChooseNotebooks.waiting_for_processors.set()

@dp.message_handler(state=ChooseNotebooks.waiting_for_screen_resolution)
async def resolution_choosed (message: types.Message,state: FSMContext):
    if message.text.lower() in available_screen_resolution_citilink:
        if message.text.lower()=='продолжить':
            text = open("data.txt").read()
            await state.update_data(chosen_resolution=text)
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            with open("data.txt","w") as f:
                f.write("")
            for matrix_type in available_matrix_type_citilink:
                keyboard.add(matrix_type)
            await message.answer('Выберете тип матрицы',reply_markup=keyboard)
            await ChooseNotebooks.waiting_for_matrix_type.set()
        else:
            with open("data.txt",'a') as f:
                f.write(message.text.lower()+',')
            await message.answer(message.text.lower())
            return
    else:
        await message.answer("Пожалуйста выберете разрешение экрана с помощью клавиатуры")
        ChooseNotebooks.waiting_for_screen_resolution.set()

@dp.message_handler(state=ChooseNotebooks.waiting_for_matrix_type)
async def matrix_choosed (message: types.Message,state: FSMContext):
    if message.text.lower() in available_matrix_type_citilink:
        if message.text.lower()=='продолжить':
            text = open("data.txt").read()
            await state.update_data(chosen_matrix=text)
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            with open("data.txt","w") as f:
                f.write("")
            for ssd_size in available_ssd_size_citilink:
                keyboard.add(ssd_size)
            await message.answer('Выберете объем SSD накопителя',reply_markup=keyboard)
            await ChooseNotebooks.waiting_for_ssd_size.set()
        else:
            with open("data.txt",'a') as f:
                f.write(message.text.lower()+',')
            await message.answer(message.text.lower())
            return
    else:
        await message.answer("Пожалуйста выберете тип матрицы с помощью клавитауты")
        ChooseNotebooks.waiting_for_matrix_type.set()

@dp.message_handler(state=ChooseNotebooks.waiting_for_ssd_size)
async def ssd_size_choosed (message: types.Message,state: FSMContext):
    if message.text.lower() in available_ssd_size_citilink:
        if message.text.lower()=='продолжить':
            text = open("data.txt").read()
            await state.update_data(chosen_ssd_size=text)
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            with open("data.txt","w") as f:
                f.write("")
            for RAM_size in available_RAM_size_citilink:
                keyboard.add(RAM_size)
            await message.answer('Выберете объем оперативной памяти',reply_markup=keyboard)
            await ChooseNotebooks.waiting_for_RAM_size.set()
        else:
            with open("data.txt",'a') as f:
                f.write(message.text.lower()+',')
            await message.answer(message.text.lower())
            return
    else:
        await message.answer("Пожалуйста выберете объем SSD с помощью клавиатуры")
        ChooseNotebooks.waiting_for_ssd_size.set()

@dp.message_handler(state=ChooseNotebooks.waiting_for_RAM_size)
async def RAM_size_choosed (message: types.Message,state: FSMContext):
    if message.text.lower() in available_RAM_size_citilink:
        if message.text.lower()=='продолжить':
            text = open("data.txt").read()
            await state.update_data(chosen_RAM_size=text)
            with open("data.txt","w") as f:
                f.write("")
            user_data = await state.get_data()
            with open('user_data.json', 'w') as file:
                json.dump(user_data, file, ensure_ascii=False, indent=1)
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            for action in available_actions:
                keyboard.add(action)
            await message.answer(f'Вы выбрали \n категория: {user_data["chosen_category"]}\n'
                                 f'минимальная цена: {user_data["chosen_min_price"]}\n'
                                 f'максимальная цена: {user_data["chosen_max_price"]}\n'
                                 f'производитель(-и): {user_data["chosen_manufacture"]}\n'
                                 f'процессор(-ы): {user_data["chosen_processor"]}\n'
                                 f'разрешение(-я) экрана: {user_data["chosen_resolution"]}\n'
                                 f'матрица(-ы) экрана: {user_data["chosen_matrix"]}\n'
                                 f'объем(-ы) ssd накопителя: {user_data["chosen_ssd_size"]}\n'
                                 f'объем(-ы) оперативки: {user_data["chosen_RAM_size"]}.\n Вывести соответствующие товары?',reply_markup=keyboard)
            await state.finish()
        else:
            with open("data.txt",'a') as f:
                f.write(message.text.lower()+',')
            await message.answer(message.text.lower())
            return
    else:
        await message.answer("Пожалуйста выберете объем оперативной памяти с помощью клавиатуры")
        await ChooseNotebooks.waiting_for_RAM_size.set()

@dp.message_handler(Text(equals='выбрать товары заново'))
async def return_to_begin(message:types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for category in available_categories:
        keyboard.add(category)
    await message.answer('Какой товар вы бы хотели найти?', reply_markup=keyboard)
    await ChooseNotebooks.waiting_for_category.set()

@dp.message_handler(Text(equals='да, вывести'))
async def parser (message: types.Message):
    await message.answer('Подождите немного')
    changing_url()
    citilink_parser()
    with open('result_data_citilink.json') as file:
        data = json.load(file)

    if data!= []:
        for item in data:
            card = f"{hlink('Ситилинк', item.get('link'))}\n" \
                    f"{hbold('Модель: ')} {item.get('name_model')}\n" \
                    f"{hbold('Цена: ')} {item.get('price')}\n"\

            photo = open(f'{way_to_directory}{item.get("name_model").replace("/","")}.jpg','rb')
            await message.answer(card)
            await bot.send_photo(chat_id=message.chat.id, photo=photo)
            nothing = []
            with open('result_data_citilink.json','w') as file:
                    json.dump(nothing,file)

        files = glob.glob(f'{way_to_directory}*')
        for f in files:
            os.remove(f)

        await message.answer('Это все ноутбуки в наличии')

    else:
        await message.answer('Ноутбуков нет в наличии. Поищите позже, или выберите другие параметры ноутбуков.')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for category in available_categories:
        keyboard.add(category)
    await message.answer('Какой товар вы бы хотели найти?', reply_markup=keyboard)
    await ChooseNotebooks.waiting_for_category.set()

def main():
    executor.start_polling(dp)

if __name__ == "__main__":
    main()
