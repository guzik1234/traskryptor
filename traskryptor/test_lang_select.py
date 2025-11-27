"""Prosty test GUI - sprawdź czy target_lang się zmienia"""
import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Test wyboru języka")
root.geometry("400x300")

target_lang = tk.StringVar(value="en")

def check_value():
    print(f"Wybrany język: {target_lang.get()}")
    result_label.config(text=f"Wybrany: {target_lang.get()}")
    
    lang_map = {"en": "_en", "ru": "_ru", "uk": "_ua"}
    suffix = lang_map.get(target_lang.get(), "_en")
    suffix_label.config(text=f"Sufiks: {suffix}")

tk.Label(root, text="Wybierz język:", font=("Arial", 12)).pack(pady=20)

tk.Radiobutton(root, text="Angielski (EN)", variable=target_lang, 
               value="en", font=("Arial", 11)).pack(anchor='w', padx=50)
tk.Radiobutton(root, text="Rosyjski (RU)", variable=target_lang, 
               value="ru", font=("Arial", 11)).pack(anchor='w', padx=50)
tk.Radiobutton(root, text="Ukraiński (UA)", variable=target_lang, 
               value="uk", font=("Arial", 11)).pack(anchor='w', padx=50)

tk.Button(root, text="Sprawdź wybór", command=check_value, 
          font=("Arial", 12), bg="#4CAF50", fg="white").pack(pady=20)

result_label = tk.Label(root, text="", font=("Arial", 11, "bold"))
result_label.pack(pady=5)

suffix_label = tk.Label(root, text="", font=("Arial", 11))
suffix_label.pack(pady=5)

root.mainloop()
