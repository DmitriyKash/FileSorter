import os
import re
import shutil
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox, ttk
import threading
from pathlib import Path

dir_suff_dict = {"Images": ['.jpg', '.jpeg', '.png', '.gif', '.tiff', '.ico', '.bmp', '.webp', '.svg'],
                 "Documents": [".md", ".epub", ".txt", ".docx", ".doc", ".ods", ".odt", ".dotx", ".docm", ".dox",
                               ".rvg", ".rtf", ".rtfd", ".wpd", ".xls", ".xlsx", ".ppt", ".pptx", ".csv", ".xml"],
                 "Archives": [".iso", ".tar", ".gz", ".7z", ".dmg", ".rar", ".zip"],
                 "Audio": [".aac", ".m4a", ".mp3", "ogg", ".raw", ".wav", ".wma"],
                 "Video": [".avi", ".flv", ".wmv", ".mov", ".mp4", ".webm", ".vob", ".mpg", ".mpeg", ".3gp"],
                 "PDF": [".pdf"],
                 "HTML": [".html", ".htm", ".xhtml"],
                 "EXE_MSI": [".exe", ".msi"],
                 }


def normalize(name: str) -> str:
    CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    TRANSLATION = (
        "a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
        "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja")

    TRANS = {}
    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()
    t_name = name.translate(TRANS)
    t_name = re.sub(r'\W', '_', t_name)
    return t_name


def sort_func(path_dir):
    cur_dir = Path(path_dir)
    dir_path = []

    for root, dirs, files in os.walk(path_dir):
        for d in dirs:
            dir_path.append(os.path.join(root, d))
        for file in files:
            p_file = Path(root) / file
            name_normalize = f"{normalize(p_file.name[0:-len(p_file.suffix)])}{p_file.suffix}"
            p_file.rename(Path(root) / name_normalize)
            p_file = Path(root) / name_normalize
            for suff in dir_suff_dict:
                if p_file.suffix.lower() in dir_suff_dict[suff]:
                    if p_file.suffix.lower() in dir_suff_dict['Archives']:
                        shutil.unpack_archive(p_file, os.path.join(cur_dir, 'Archives', p_file.name))

                    dir_img = cur_dir / suff
                    dir_img.mkdir(exist_ok=True)

                    try:
                        p_file.rename(dir_img.joinpath(p_file.name))
                    except FileExistsError:
                        p_file.rename(dir_img.joinpath(f'{p_file.name.split(".")[0]}_c{p_file.suffix}'))
                        update_log(f"Возможно дубликат: {p_file.name}")

    for dir_p in reversed(dir_path):
        if os.path.split(dir_p)[1] in dir_suff_dict or os.stat(dir_p).st_size != 0:
            continue
        else:
            os.rmdir(dir_p)


def update_log(message):
    text_log.config(state='normal')
    text_log.insert(tk.END, message + "\n")
    text_log.config(state='disabled')
    text_log.see(tk.END)


def start_sorting(path):
    update_log("Сортируем файли...")
    if not Path(path).exists():
        messagebox.showerror("Ошибка", "Директории не существует")
        update_log("Ошибка: директории не существует")
    else:
        sort_func(path)  # Тут можна додати логування всередині sort_func, використовуючи update_log
        update_log("Сортировка завершена")


def browse_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        label_info.config(text=f"Выбранная директория: {folder_selected}")
        button_sort.config(command=lambda: threading.Thread(target=start_sorting, args=(folder_selected,)).start())


root = tk.Tk()
root.title("File Sorter")

label_info = tk.Label(root, text="Выберите папку для сортировки:")
label_info.pack()

button_browse = tk.Button(root, text="Выбрать папку", command=browse_folder)
button_browse.pack()

button_sort = tk.Button(root, text="Начать сортировку")
button_sort.pack()

text_log = scrolledtext.ScrolledText(root, height=10, wrap=tk.WORD)
text_log.pack()

root.mainloop()
