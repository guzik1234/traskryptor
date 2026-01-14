"""
Główna aplikacja - wybór między transkrypcją a tłumaczeniem
"""
import tkinter as tk
from tkinter import messagebox
import traceback
import sys


class MainApp:
    """Główne menu aplikacji"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Transkrypcja i Tłumaczenie")
        self.root.geometry("550x600")
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
        button_frame.pack(pady=20)
        
        # Przycisk transkrypcji z pliku audio
        audio_file_btn = tk.Button(
            button_frame,
            text=" Transkrypcja z pliku audio\n(Audio  DOCX + PDF)",
            command=self.open_audio_file_transcription,
            font=("Arial", 13, "bold"),
            bg="#9C27B0",
            fg="white",
            width=30,
            height=3,
            cursor="hand2"
        )
        audio_file_btn.pack(pady=10)
        
        # Przycisk transkrypcji na żywo
        transcription_btn = tk.Button(
            button_frame,
            text=" Transkrypcja na żywo\n(Mowa  Word)",
            command=self.open_transcription,
            font=("Arial", 13, "bold"),
            bg="#4CAF50",
            fg="white",
            width=30,
            height=3,
            cursor="hand2"
        )
        transcription_btn.pack(pady=10)
        
        # Przycisk tłumaczenia PDF/Word
        translation_btn = tk.Button(
            button_frame,
            text="📄 Tłumaczenie dokumentów\n(Word/PDF → Polski/Angielski)",
            command=self.open_translation,
            font=("Arial", 13, "bold"),
            bg="#2196F3",
            fg="white",
            width=30,
            height=3,
            cursor="hand2"
        )
        translation_btn.pack(pady=10)
        
        # Informacja o offline
        info_label = tk.Label(
            button_frame,
            text="💡 Tłumaczenie działa offline po pierwszym pobraniu modeli",
            font=("Arial", 9),
            fg="gray"
        )
        info_label.pack(pady=5)
        
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
    
    def open_audio_file_transcription(self):
        """Otwiera moduł transkrypcji z pliku audio"""
        try:
            self.root.destroy()
            from audio_file_transcription import AudioFileTranscriptionGUI
            
            gui = AudioFileTranscriptionGUI()
            gui.run()
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się uruchomić transkrypcji z pliku:\n{str(e)}\n\n{traceback.format_exc()}")
    
    def open_transcription(self):
        """Otwiera moduł transkrypcji na żywo"""
        try:
            self.root.destroy()
            from gui import TranscriptionGUI
            from speech_to_word import run_transcription
            
            gui = TranscriptionGUI(
                on_start_callback=run_transcription,
                on_stop_callback=None
            )
            gui.run()
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się uruchomić transkrypcji na żywo:\n{str(e)}\n\n{traceback.format_exc()}")
    
    def open_translation(self):
        """Otwiera moduł tłumaczenia"""
        try:
            self.root.destroy()
            from translation_gui import TranslationGUI
            
            gui = TranslationGUI()
            gui.run()
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się uruchomić modułu tłumaczenia:\n{str(e)}\n\n{traceback.format_exc()}")
    
    def run(self):
        """Uruchamia aplikację"""
        self.root.mainloop()


if __name__ == "__main__":
    try:
        app = MainApp()
        app.run()
    except Exception as e:
        messagebox.showerror("Błąd krytyczny", f"Aplikacja napotkała nieoczekiwany błąd:\n{str(e)}\n\n{traceback.format_exc()}")
