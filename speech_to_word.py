import time
import keyboard

from gui import TranscriptionGUI
from audio_handler import AudioHandler
from transcription_model import TranscriptionModel
from word_handler import WordHandler


def run_transcription(gui):
    """Główna funkcja transkrypcji uruchamiana w osobnym wątku"""
    audio = None
    word = None
    
    try:
        # Ładowanie modelu (używamy domyślnego modelu "1")
        model = TranscriptionModel(gui.selected_language, "1")
        
        # Inicjalizacja audio
        audio = AudioHandler()
        audio.start()
        
        # Połączenie z Word
        word = WordHandler()
        if not word.connect():
            print("Otwórz Worda przed uruchomieniem skryptu.")
            gui.update_status("Błąd: Otwórz Word!", "red")
            gui.enable_buttons()
            if audio:
                audio.stop()
            return
        
        gui.update_status("Nasłuchiwanie aktywne...", "green")
        print("READY — wciśnij i trzymaj Lewy Shift, by nagrywać.")
        
        # Główna pętla nasłuchiwania
        while not gui.should_stop:
            if keyboard.is_pressed("left shift"):
                print("Nagrywanie...")
                frames = []
                
                while keyboard.is_pressed("left shift") and not gui.should_stop:
                    data = audio.read()
                    frames.append(data)
                
                if frames:
                    print("Przetwarzanie...")
                    audio_np = audio.process_audio(frames)
                    
                    try:
                        text = model.transcribe(audio_np, audio.rate)
                        
                        if text:
                            print("Transkrypcja:", text)
                            word.insert_text(text)
                    except Exception as e:
                        print("Błąd transkrypcji:", e)
            
            time.sleep(0.1)
        
        print("Zatrzymano.")
        
    except Exception as e:
        print("Błąd:", e)
        gui.update_status(f"Błąd: {str(e)}", "red")
        gui.enable_buttons()
    finally:
        if audio:
            audio.stop()


def main():
    """Główna funkcja aplikacji"""
    gui = TranscriptionGUI(
        on_start_callback=run_transcription,
        on_stop_callback=None
    )
    gui.run()


if __name__ == "__main__":
    main()
