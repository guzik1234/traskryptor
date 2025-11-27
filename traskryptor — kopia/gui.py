import tkinter as tk
import threading


class TranscriptionGUI:
    """Interfejs graficzny dla aplikacji transkrypcji"""
    
    def __init__(self, on_start_callback, on_stop_callback):
        self.root = tk.Tk()
        self.root.title("Transkrypcja mowy do tekstu")
        self.root.geometry("550x500")
        self.root.resizable(False, False)
        
        self.on_start_callback = on_start_callback
        self.on_stop_callback = on_stop_callback
        
        self.selected_language = None
        self.selected_model = None
        self.is_running = False
        self.should_stop = False
        
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
                      font=("Arial", 13), command=self.update_model_options).pack(anchor='w', padx=50, pady=5)
        tk.Radiobutton(self.lang_frame, text="Angielski", variable=self.lang_var, value="angielski",
                      font=("Arial", 13), command=self.update_model_options).pack(anchor='w', padx=50, pady=5)
        
        # Model (widoczny tylko dla polskiego)
        self.model_frame = tk.Frame(self.root)
        
        tk.Label(self.model_frame, text="Wybierz model:", font=("Arial", 14, "bold")).pack(pady=(10, 5))
        
        self.model_var = tk.StringVar(value="1")
        tk.Radiobutton(self.model_frame, text="Model 1 (Small - szybszy)", 
                      variable=self.model_var, value="1", font=("Arial", 13)).pack(anchor='w', padx=50, pady=5)
        tk.Radiobutton(self.model_frame, text="Model 2 (Medium - dokładniejszy)", 
                      variable=self.model_var, value="2", font=("Arial", 13)).pack(anchor='w', padx=50, pady=5)
        
        # Przyciski - zawsze na dole
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(side=tk.BOTTOM, pady=20)
        
        self.start_button = tk.Button(self.button_frame, text="Start", command=self._on_start_clicked, 
                 font=("Arial", 14, "bold"), bg="#4CAF50", fg="white", 
                 width=18, height=2)
        self.start_button.pack(pady=5)
        
        self.stop_button = tk.Button(self.button_frame, text="Zakończ nasłuchiwanie", command=self._on_stop_clicked, 
                 font=("Arial", 14, "bold"), bg="#f44336", fg="white", 
                 width=18, height=2, state="disabled")
        self.stop_button.pack(pady=5)
        
        # Status - nad przyciskami
        self.status_label = tk.Label(self.root, text="Wybierz opcje i naciśnij Start", 
                                     font=("Arial", 11), fg="gray")
        self.status_label.pack(side=tk.BOTTOM, pady=(0, 10))
        
        self.update_model_options()
        
    def update_model_options(self):
        """Pokazuje/ukrywa opcje wyboru modelu w zależności od języka"""
        if self.lang_var.get() == "polski":
            self.model_frame.pack(after=self.lang_frame, pady=10)
        else:
            self.model_frame.pack_forget()
    
    def _on_start_clicked(self):
        """Obsługa kliknięcia przycisku Start"""
        self.selected_language = self.lang_var.get()
        self.selected_model = self.model_var.get() if self.selected_language == "polski" else None
        self.is_running = True
        self.should_stop = False
        
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.update_status("Ładowanie modelu...", "orange")
        
        # Uruchom transkrypcję w osobnym wątku
        transcription_thread = threading.Thread(target=self.on_start_callback, args=(self,), daemon=True)
        transcription_thread.start()
    
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
    
    def run(self):
        """Uruchamia główną pętlę GUI"""
        self.root.mainloop()
