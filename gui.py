import tkinter as tk
import threading


class TranscriptionGUI:
    """Interfejs graficzny dla aplikacji transkrypcji"""
    
    def __init__(self, on_start_callback, on_stop_callback):
        self.root = tk.Tk()
        self.root.title("Transkrypcja mowy do tekstu")
        self.root.geometry("700x900")
        self.root.resizable(False, False)
        
        self.on_start_callback = on_start_callback
        self.on_stop_callback = on_stop_callback
        
        self.selected_language = None
        self.is_running = False
        self.should_stop = False
        self.translate_enabled = False
        self.translate_lang = None
        
        self._create_widgets()
        
    def _create_widgets(self):
        """Tworzy wszystkie widgety interfejsu"""
        # Język
        lang_label = tk.Label(self.root, text="Wybierz język:", font=("Arial", 14, "bold"))
        lang_label.pack(pady=15)
        
        self.lang_frame = tk.Frame(self.root)
        self.lang_frame.pack()
        
        self.lang_var = tk.StringVar(value="polski")
        tk.Radiobutton(self.lang_frame, text="Polski", variable=self.lang_var, value="polski", 
                      font=("Arial", 13)).pack(anchor='w', padx=50, pady=5)
        tk.Radiobutton(self.lang_frame, text="Angielski", variable=self.lang_var, value="angielski",
                      font=("Arial", 13)).pack(anchor='w', padx=50, pady=5)
        
        # Opcja tłumaczenia
        self.translate_frame = tk.Frame(self.root)
        self.translate_frame.pack(pady=15)
        
        tk.Label(self.translate_frame, text="Automatyczne tłumaczenie:", font=("Arial", 14, "bold")).pack(pady=(0, 5))
        
        self.translate_var = tk.BooleanVar(value=False)
        tk.Checkbutton(self.translate_frame, text="Włącz tłumaczenie transkrypcji", 
                      variable=self.translate_var, font=("Arial", 12),
                      command=self.update_translate_options).pack(anchor='w', padx=50, pady=5)
        
        # Wybór języka tłumaczenia (pokazuje się po zaznaczeniu checkboxa)
        self.translate_lang_frame = tk.Frame(self.translate_frame)
        
        tk.Label(self.translate_lang_frame, text="Przetłumacz na:", font=("Arial", 11)).pack(anchor='w', padx=70, pady=(5, 0))
        
        self.translate_lang_var = tk.StringVar(value="en")
        tk.Radiobutton(self.translate_lang_frame, text="Angielski", variable=self.translate_lang_var, 
                      value="en", font=("Arial", 11)).pack(anchor='w', padx=90, pady=2)
        tk.Radiobutton(self.translate_lang_frame, text="Rosyjski", variable=self.translate_lang_var, 
                      value="ru", font=("Arial", 11)).pack(anchor='w', padx=90, pady=2)
        tk.Radiobutton(self.translate_lang_frame, text="Ukraiński", variable=self.translate_lang_var, 
                      value="uk", font=("Arial", 11)).pack(anchor='w', padx=90, pady=2)
        
        # Przyciski - zawsze na dole
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(side=tk.BOTTOM, pady=20)
        
        
        self.start_button = tk.Button(self.button_frame, text="Start", command=self._on_start_clicked, 
                 font=("Arial", 14, "bold"), bg="#4CAF50", fg="white", 
                 width=22, height=2)
        self.start_button.pack(pady=5, fill='x')
        
        self.stop_button = tk.Button(self.button_frame, text="Zakończ nasłuchiwanie", command=self._on_stop_clicked, 
                 font=("Arial", 14, "bold"), bg="#f44336", fg="white", 
                 width=22, height=2, state="disabled")
        self.stop_button.pack(pady=5, fill='x')

        self.back_button = tk.Button(self.button_frame, text="Powrót do menu", 
                          command=self._on_back_clicked,
                          font=("Arial", 11), bg="#FF9800", 
                          fg="white", width=22, height=1)
        self.back_button.pack(pady=10, fill='x')
        
        # Dodatkowa pusta przestrzeń pod przyciskami (100px)
        self.bottom_spacer = tk.Frame(self.button_frame, height=200)
        self.bottom_spacer.pack(fill='x')
        self.bottom_spacer.pack_propagate(False)

    
        # Status - nad przyciskami
        self.status_label = tk.Label(self.root, text="Wybierz opcje i naciśnij Start", 
                                     font=("Arial", 11), fg="gray")
        self.status_label.pack(side=tk.BOTTOM, pady=(0, 10))
    
    def update_translate_options(self):
        """Pokazuje/ukrywa opcje języka tłumaczenia"""
        if self.translate_var.get():
            self.translate_lang_frame.pack(pady=5)
        else:
            self.translate_lang_frame.pack_forget()
    
    def _on_start_clicked(self):
        """Obsługa kliknięcia przycisku Start"""
        self.selected_language = self.lang_var.get()
        self.translate_enabled = self.translate_var.get()
        self.translate_lang = self.translate_lang_var.get() if self.translate_enabled else None
        self.is_running = True
        self.should_stop = False
        
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        
        status_text = "Ładowanie modelu..."
        if self.translate_enabled:
            status_text += f" + translator ({self.translate_lang.upper()})"
        self.update_status(status_text, "orange")
        
        # Uruchom transkrypcję w osobnym wątku
        transcription_thread = threading.Thread(target=self.on_start_callback, args=(self,), daemon=True)
        transcription_thread.start()
    
    def _on_back_clicked(self):
        """Obsługa kliknięcia przycisku Powrót"""
        self.root.destroy()
        from main import MainApp
        app = MainApp()
        app.run()
    
    def _on_stop_clicked(self):
        """Obsługa kliknięcia przycisku Stop"""
        self.should_stop = True
        self.is_running = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.update_status("Nasłuchiwanie zatrzymane", "red")
        
        if self.on_stop_callback:
            self.on_stop_callback()
    
    def update_status(self, text, color="gray"):
        """Aktualizuje tekst statusu"""
        self.root.after(0, lambda: self.status_label.config(text=text, fg=color))
    
    def enable_buttons(self):
        """Włącza przyciski po błędzie"""
        self.root.after(0, lambda: self.start_button.config(state="normal"))
        self.root.after(0, lambda: self.stop_button.config(state="disabled"))
    def _on_back_clicked(self):
        """Obsługa kliknięcia przycisku Powrót"""
        self.root.destroy()
        from main import MainApp
        app = MainApp()
        app.run()
    
    def run(self):
        """Uruchamia główną pętlę GUI"""
        self.root.mainloop()


