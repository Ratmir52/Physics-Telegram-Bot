from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

keyboard = [
        [InlineKeyboardButton("Перевод частоты и энергии в длинну волны", callback_data='button1')],
        [InlineKeyboardButton("Вычислить флюенс", callback_data='button2')] 

     ]

reply_markup = InlineKeyboardMarkup(keyboard)

async def greet_user(update: Update, ) -> None:
    
    welcome_message = (
        "<b>Привет! Я ваш научный ассистент. Вот что я могу сделать: </b>\n\n"
        "<b>1.</b>  Переводить частоту или энергию <a href='https://ru.wikipedia.org/wiki/%D0%A4%D0%BE%D1%82%D0%BE%D0%BD'>фотона</a> в длину волны и обратно. \n\n"
        "<b>2.</b>  Анализировать <a href='https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B5%D0%BA%D1%82%D1%80'>спектры</a> и выводить графики. \n\n"
        "<b>3.</b>  Вычислять <a href='https://ru.wikipedia.org/wiki/%D0%A4%D0%BB%D1%8E%D0%B5%D0%BD%D1%81'>флюенс</a> лазерной системы. \n\n"
        "<b>Чтобы узнать команды введите /help!</b>"

    )
    await update.message.reply_text(welcome_message, parse_mode='HTML', disable_web_page_preview=True, reply_markup=reply_markup)

def convert_frequency_to_wavelength(frequency):
    c = 3e8
    wavelenght = (c / frequency) * 1e6
    return wavelenght
def convert_energy_to_wavelength(energy):
    h = 6.626e-34
    c = 3e8
    wavelenght = h * c / energy
    return wavelenght * 1e6

async def help_to_user(update: Update):

    message = (
        "<b>/start</b> - перезапуск бота. \n\n"
        "<b>Отправьте текстовый документ чтобы вычислить положения резонанса и его ширины на полувысоте по спектру и составить график.</b> \n\n"
        )
    await update.message.reply_text(message, parse_mode='HTML', disable_web_page_preview=True, reply_markup=reply_markup)

def fluence_calculation(P, t, A):
    fluence = P * t / A     # Формула флюенса
    return fluence

async def feedback(update: Update):
    message = (
        "<b>Прежде чем продолжить...</b>\n\n"
        "<b>Оставьте отзыв о нашем боте!</b>\n\n"
        "<b>И все ваши пожелания будут переданы разработчику и добавлены бота!</b>\n\n"
        "<b>Введите Y чтобы оставить отзыв или n для выхода!</b> \n\n"
        )
    await update.message.reply_text(message, parse_mode='HTML', disable_web_page_preview=True)

async def range_inf(update: Update):
    range_message = (
        "<b>Диапазоны длин волн:</b>\n\n"
        "1.<b>Радиоволны: 1 мм - 100 км.</b>\n\n"
        "2.<b>Микроволны: 1 мм - 1 м.</b>\n\n"
        "3.<b>Инфракрасное излучение: 700 нм - 1 мм.</b>\n\n"
        "4.<b>Видимый свет: 400 нм - 700 нм.</b>\n\n"
        "5.<b>Ультрафиолетовое излучение: 10 нм - 400 нм.</b>\n\n"
        "6.<b>Рентгеновские лучи: 0.01 нм - 10 нм.</b>\n\n"
        "7.<b>Гамма - лучи: меньше 0.01 нм.</b>"
        )
    await update.message.reply_text(range_message, parse_mode='HTML')