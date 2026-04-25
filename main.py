import tkinter as tk
from tkinter import messagebox, ttk
import requests
import json
import os

# Файл для хранения избранных
FAV_FILE = "favorites.json"

class GitHubUserFinderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GitHub User Finder")
        self.root.geometry("400x500")

        # 1. Поле ввода
        self.search_entry = ttk.Entry(root, width=30)
        self.search_entry.pack(pady=10)

        search_btn = ttk.Button(root, text="Найти", command=self.search_user)
        search_btn.pack()

        # 2. Результаты поиска
        self.result_label = ttk.Label(root, text="", wraplength=350, justify="center")
        self.result_label.pack(pady=10)

        # 3. Кнопка Избранное
        self.fav_btn = ttk.Button(root, text="Добавить в избранное", command=self.add_to_favorites)
        self.fav_btn.pack(pady=5)
        self.fav_btn.pack_forget() # Скрыть до поиска

        # Список избранных
        ttk.Label(root, text="Избранные:").pack(pady=5)
        self.fav_listbox = tk.Listbox(root, width=50, height=10)
        self.fav_listbox.pack(pady=5)
        
        self.current_user = None
        self.load_favorites_from_file()

    def search_user(self):
        username = self.search_entry.get().strip()
        
        # 5. Проверка ввода
        if not username:
            messagebox.showwarning("Ошибка", "Поле поиска не должно быть пустым")
            return

        url = f"https://api.github.com/users/{username}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                self.current_user = response.json()
                self.result_label.config(text=f"User: {self.current_user['login']}\n"
                                             f"Repos: {self.current_user['public_repos']}\n"
                                             f"Bio: {self.current_user['bio']}")
                self.fav_btn.pack() # Показать кнопку
            else:
                self.result_label.config(text="Пользователь не найден")
                self.fav_btn.pack_forget()
                self.current_user = None
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка подключения: {e}")

    # 3. Добавление в избранное
    def add_to_favorites(self):
        if not self.current_user: return
        
        username = self.current_user['login']
        if username not in self.fav_listbox.get(0, tk.END):
            self.fav_listbox.insert(tk.END, username)
            self.save_favorites_to_json()
        
    # 4. Сохранение в JSON
    def save_favorites_to_json(self):
        favorites = self.fav_listbox.get(0, tk.END)
        with open(FAV_FILE, "w") as f:
            json.dump(list(favorites), f)

    def load_favorites_from_file(self):
        if os.path.exists(FAV_FILE):
            with open(FAV_FILE, "r") as f:
                try:
                    favorites = json.load(f)
                    for user in favorites:
                        self.fav_listbox.insert(tk.END, user)
                except:
                    pass

if __name__ == "__main__":
    root = tk.Tk()
    app = GitHubUserFinderApp(root)
    root.mainloop()
