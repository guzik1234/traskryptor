"""
Główna aplikacja - wybór między transkrypcją a tłumaczeniem
"""
import tkinter as tk


class MainApp:
    """Główne menu aplikacji"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Transkrypcja i Tłumaczenie")
        self.root.geometry("500x350")
        self.root.resizable(False, False)
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Tworzy widgety głównego menu"""
        
        # Tytuł
        title = tk.Label(self.root, text="Wybierz funkcję", 
                        font=("Arial", 18, "bold"))
        title.pack(pady=30)
        
        # Opis
        desc = tk.Label(self.root, 
                       text="Co chcesz zrobić?",
                       font=("Arial", 12))
        desc.pack(pady=10)
        
        # Przyciski
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=30)
        
        # Przycisk transkrypcji
        transcription_btn = tk.Button(
            button_frame,
            text="📝 Transkrypcja mowy\n(Mowa → Word)",
            command=self.open_transcription,
            font=("Arial", 13, "bold"),
            bg="#4CAF50",
            fg="white",
            width=25,
            height=3,
            cursor="hand2"
        )
        transcription_btn.pack(pady=10)
        
        # Przycisk tłumaczenia
        translation_btn = tk.Button(
            button_frame,
            text="🌍 Tłumaczenie PDF\n(Polski → Angielski/Rosyjski)",
            command=self.open_translation,
            font=("Arial", 13, "bold"),
            bg="#2196F3",
            fg="white",
            width=25,
            height=3,
            cursor="hand2"
        )
        translation_btn.pack(pady=10)
        
        # Przycisk wyjścia
        exit_btn = tk.Button(
            button_frame,
            text="Wyjście",
            command=self.root.quit,
            font=("Arial", 11),
            bg="#f44336",
            fg="white",
            width=15,
            height=1
        )
        exit_btn.pack(pady=20)
    
    def open_transcription(self):
        """Otwiera moduł transkrypcji"""
        self.root.destroy()
        from gui import TranscriptionGUI
        from speech_to_word import run_transcription
        
        gui = TranscriptionGUI(
            on_start_callback=run_transcription,
            on_stop_callback=None
        )
        gui.run()
    
    def open_translation(self):
        """Otwiera moduł tłumaczenia"""
        self.root.destroy()
        from translation_gui import TranslationGUI
        
        gui = TranslationGUI()
        gui.run()
    
    def run(self):
        """Uruchamia aplikację"""
        self.root.mainloop()


if __name__ == "__main__":
    app = MainApp()
    app.run()
