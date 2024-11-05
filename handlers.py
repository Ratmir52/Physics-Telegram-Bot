
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils import greet_user, convert_frequency_to_wavelength, help_to_user, fluence_calculation, feedback, convert_energy_to_wavelength, range_inf
from analyze_spectrum import analyze_spectrum
import json


USER_STATE = {}
RATED_USERS = {}


keyboard = [
        [InlineKeyboardButton("Перевод частоты и энергии в длинну волны", callback_data='button1')],
        [InlineKeyboardButton("Вычислить флюенс", callback_data='button2')] 

     ]

reply_markup = InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    USER_STATE[str(user_id)] = "none"
    await greet_user(update)


async def convert(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.callback_query.from_user.id
    await update.callback_query.message.reply_text("Пожалуйста, введите частоту и единицу измерения (например, '3000000000 Hz').")
    USER_STATE[str(user_id)] = "is_convert"

   

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id

    if str(user_id) not in USER_STATE:
        USER_STATE[str(user_id)] = "none"

    if USER_STATE[str(user_id)] == "none":
        return

    if USER_STATE[str(user_id)] == "is_convert":

        text = update.message.text
        args = text.split()
        print(text, args, user_id)

        if len(args) < 2:
            await update.message.reply_text("Пожалуйста, укажите частоту и единицу измерения (Hz или nm). Пример: '3000000000 Hz'", reply_markup=reply_markup)
            USER_STATE[str(user_id)] = "none"
            return

        try:
            value = float(args[0])
            print(value)
        except ValueError:
            await update.message.reply_text("Недопустимое значение. Пожалуйста, введите число.", reply_markup=reply_markup)
            USER_STATE[str(user_id)] = "none"
            return

        unit = args[1].lower()
        print(unit)

        if unit == 'hz':
            wavelength = convert_frequency_to_wavelength(value)
            await update.message.reply_text(f"Длина волны: {wavelength:.2f} мкм", reply_markup=reply_markup)
            USER_STATE[str(user_id)] = "none"
            await range_info(update)
            await feedback_dev(update,context)
        elif unit == 'nm':
            frequency = 3e8 / (value * 1e-9)  # Преобразование длины волны в частоту
            energy = (6.626e-34 * 3e8) / (value * 1e9)
            await update.message.reply_text(f"Частота: {frequency:.2f} Гц, Энергия: {energy:.2e} Дж", reply_markup=reply_markup)
            USER_STATE[str(user_id)] = "none"
            await range_info(update)
            await feedback_dev(update,context)
        elif unit == 'dz':
            wavelength = convert_energy_to_wavelength(value)
            await update.message.reply_text(f"Длина волны: {wavelength:.2e} мкм", reply_markup=reply_markup)
            USER_STATE[str(user_id)] = "none"
            await range_info(update)
            await feedback_dev(update,context)
        else:
            await update.message.reply_text("Недопустимая единица измерения. Используйте 'Hz' или 'nm'.", reply_markup=reply_markup)
            USER_STATE[str(user_id)] = "none"
            return

    elif USER_STATE[str(user_id)] == "in_fluence":
        text = update.message.text
        args = text.split()

        if len(args) < 3:
            await update.message.reply_text("Пожалуйста, укажите среднюю мощность лазера, длительность импульса, и площадь. Пример: '10 0.5 0.01'", reply_markup=reply_markup)
            USER_STATE[str(user_id)] = "none"
            return
        power = float(args[0])
        time = float(args[1])
        square = float(args[2])

        fluence = fluence_calculation(power, time, square)

        await update.message.reply_text(f"Флюэнс со значениями 'Средняя мощность: {power}, длительность импульса: {time}, площадь: {square}' будет равно {fluence} Дж/м^2", reply_markup=reply_markup)
        USER_STATE[str(user_id)] = "none"
        await range_info(update)
        await feedback_dev(update,context)

    elif USER_STATE[str(user_id)] == "feedback":

        text = update.message.text

        if text.lower() == "y":
            USER_STATE[str(user_id)] = "feedback_input"
            await update.message.reply_text("Пожалуйста, введите ваш отзыв и что бы вы хотели добавить!")
        elif text.lower() == "n":

            USER_STATE[str(user_id)] = "none"
            return

        else:
           await update.message.reply_text("Пожалуйста, введите Y или n!")
           return

    elif USER_STATE[str(user_id)] == "feedback_input":

        

        with open("feedbacks.json", "r", encoding='utf-8') as f:
            try:
                message = json.load(f)
            except json.JSONDecodeError:
                message = {}

        message[str(user_id)] = update.message.text


        with open("feedbacks.json", "w", encoding='utf-8') as f:
            json.dump(message, f,  ensure_ascii=False, indent=4)
            f.close()

        await update.message.reply_text("Спасибо за оставление отзыва", reply_markup=reply_markup)
        RATED_USERS[str(user_id)] = True
        USER_STATE[str(user_id)] = "none"
        return

    

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await analyze_spectrum(update)

async def user_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await help_to_user(update)

async def fluence(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.callback_query.from_user.id
    await update.callback_query.message.reply_text("Пожалуйста, укажите среднюю мощность лазера, длительность импульса, и площадь. Пример: '10 0.5 0.01'")
    USER_STATE[str(user_id)] = "in_fluence"

async def feedback_dev(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id



    if str(user_id) not in RATED_USERS:
        RATED_USERS[str(user_id)] = False

    if RATED_USERS[str(user_id)] == False:
        
        await feedback(update)
        USER_STATE[str(user_id)] = "feedback"
    else:
        return

async def buttons_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = update.callback_query.from_user.id

    if query.data == 'button1':
        await convert(update, context)
    elif query.data == 'button2':
        await fluence(update, context)

async def range_info(update: Update):
    await range_inf(update)