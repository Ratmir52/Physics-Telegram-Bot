from telegram import Update
from telegram.ext import ContextTypes
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks, peak_widths
import io

async def analyze_spectrum(update: Update):

    file = await update.message.document.get_file()
    await file.download_to_drive('spectrum.txt')

# Чтение данных из файла
    data = np.loadtxt('spectrum.txt')

# Длина волн и интенсивность
    wavelengths = data[:, 0]
    intensities = data[:, 1]

# Поиск пиков
    peaks, _ = find_peaks(intensities)

    if len(peaks) == 0:
        await update.message.reply_text('Пики не найдены.')
    else:
        # Нахождение ширины на полувысоте
        results_half = peak_widths(intensities, peaks, rel_height=0.5)
        peak_widths_nm = results_half[0] * (wavelengths[1] - wavelengths[0])  # ширина в единицах длин волн

        min_wavelenght = wavelengths.min() - 5
        max_wavelenght = wavelengths.max() + 5

        # Создание графика
        plt.figure(figsize=(10, 6))
        plt.plot(wavelengths, intensities, label='Спектр')
        plt.plot(wavelengths[peaks], intensities[peaks], "x", label='Пики')
        plt.hlines(*results_half[1:], color="C2")  # Линии на полувысоте
        plt.xlim(min_wavelenght,max_wavelenght)

        plt.title('Анализ спектра')
        plt.xlabel('Длина волны (нм)')
        plt.ylabel('Интенсивность')
        plt.legend()

    # Сохранение графика в буфер
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()

    # Отправка графика и результатов
        await update.message.reply_photo(photo=buf)
        result_message = '\n'.join([f'Пик на {wavelengths[peaks[i]]:.2f} нм, ширина на полувысоте: {peak_widths_nm[i]:.2f} нм' for i in range(len(peaks))])
        await update.message.reply_text(result_message)
