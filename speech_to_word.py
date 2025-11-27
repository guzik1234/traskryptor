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
    translator = None
    translator_type = None  # 'argos' lub 'nllb'
    nllb_translator = None
    
    try:
        # Ładowanie modelu transkrypcji
        model = TranscriptionModel(gui.selected_language, gui.selected_model)
        
        # Ładowanie translatora jeśli włączono tłumaczenie
        if gui.translate_enabled:
            src_lang = "pl" if gui.selected_language == "polski" else "en"
            print(f"Inicjalizacja tłumaczenia: {src_lang.upper()} → {gui.translate_lang.upper()}")
            
            # Dla RU i UK: próbuj najpierw Argos, potem NLLB fallback
            if gui.translate_lang in {"ru", "uk"}:
                # Próba 1: Argos Translate (jeśli dostępny)
                try:
                    import argostranslate.translate
                    
                    # Sprawdź czy jest para językowa
                    installed = argostranslate.translate.get_installed_languages()
                    has_pair = False
                    for src in installed:
                        for tgt in installed:
                            if src.code == src_lang and tgt.code == gui.translate_lang:
                                has_pair = True
                                break
                    
                    if has_pair:
                        translator = argostranslate.translate
                        translator_type = 'argos'
                        print(f"✓ [ARGOS] Translator gotowy: {src_lang} → {gui.translate_lang}")
                    else:
                        raise Exception(f"Brak pary językowej {src_lang}→{gui.translate_lang} w Argos")
                        
                except Exception as e:
                    print(f"⚠ [ARGOS] {e}")
                    
                    # Próba 2: NLLB Fallback
                    try:
                        print(f"[FALLBACK] Ładowanie modelu NLLB dla {src_lang}→{gui.translate_lang}...")
                        from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
                        import torch
                        
                        model_name = "facebook/nllb-200-distilled-600M"
                        tokenizer = AutoTokenizer.from_pretrained(model_name)
                        nllb_model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
                        
                        lang_map = {"pl": "pol_Latn", "en": "eng_Latn", "ru": "rus_Cyrl", "uk": "ukr_Cyrl"}
                        nllb_src_lang = lang_map.get(src_lang)
                        nllb_tgt_lang = lang_map.get(gui.translate_lang)
                        
                        nllb_translator = {
                            'tokenizer': tokenizer,
                            'model': nllb_model,
                            'src_lang': nllb_src_lang,
                            'tgt_lang': nllb_tgt_lang
                        }
                        translator_type = 'nllb'
                        print(f"✓ [NLLB] Translator gotowy: {src_lang} → {gui.translate_lang}")
                        
                    except Exception as e2:
                        print(f"✗ [NLLB] Błąd: {e2}")
                        gui.update_status("Błąd: Brak tłumaczenia!", "red")
            
            # Dla EN i PL: tylko Argos
            else:
                try:
                    import argostranslate.translate
                    
                    # Sprawdź czy jest para językowa
                    installed = argostranslate.translate.get_installed_languages()
                    has_pair = False
                    for src in installed:
                        for tgt in installed:
                            if src.code == src_lang and tgt.code == gui.translate_lang:
                                has_pair = True
                                break
                    
                    if has_pair:
                        translator = argostranslate.translate
                        translator_type = 'argos'
                        print(f"✓ [ARGOS] Translator gotowy: {src_lang} → {gui.translate_lang}")
                    else:
                        print(f"⚠ [ARGOS] Brak pary językowej {src_lang}→{gui.translate_lang}")
                        print(f"Uruchom: python install_languages.py")
                        gui.update_status("Błąd: Brak pakietów językowych! Uruchom install_languages.py", "red")
                        gui.enable_buttons()
                        if audio:
                            audio.stop()
                        return
                        
                except Exception as e:
                    print(f"✗ [ARGOS] {e}")
                    print(f"Uruchom: python install_languages.py")
                    gui.update_status("Błąd: Brak pakietów językowych! Uruchom install_languages.py", "red")
                    gui.enable_buttons()
                    if audio:
                        audio.stop()
                    return
        
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
        
        status_msg = "Nasłuchiwanie aktywne"
        if gui.translate_enabled:
            src_lang = "PL" if gui.selected_language == "polski" else "EN"
            trans_type = "ARGOS" if translator_type == 'argos' else "NLLB"
            status_msg += f" + Tłumaczenie {src_lang}→{gui.translate_lang.upper()} [{trans_type}]"
        gui.update_status(status_msg, "green")
        print(f"READY — wciśnij i trzymaj Lewy Shift, by nagrywać.")
        if gui.translate_enabled:
            src_lang = "polski" if gui.selected_language == "polski" else "angielski"
            trans_type = "Argos" if translator_type == 'argos' else "NLLB Fallback"
            print(f"Tłumaczenie automatyczne ({trans_type}): {src_lang} → {gui.translate_lang}")
        
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
                            print(f"Transkrypcja: {text}")
                            
                            # Jeśli włączono tłumaczenie - przetłumacz tekst
                            if gui.translate_enabled and (translator or nllb_translator):
                                try:
                                    translated_text = None
                                    src_lang_code = "pl" if gui.selected_language == "polski" else "en"
                                    
                                    # Tłumaczenie przez Argos
                                    if translator_type == 'argos' and translator:
                                        translated_text = translator.translate(
                                            text, 
                                            src_lang_code, 
                                            gui.translate_lang
                                        )
                                    
                                    # Tłumaczenie przez NLLB
                                    elif translator_type == 'nllb' and nllb_translator:
                                        tokenizer = nllb_translator['tokenizer']
                                        nllb_model = nllb_translator['model']
                                        src_lang = nllb_translator['src_lang']
                                        tgt_lang = nllb_translator['tgt_lang']
                                        
                                        tokenizer.src_lang = src_lang
                                        inputs = tokenizer(text, return_tensors="pt", truncation=True)
                                        forced_bos = tokenizer.convert_tokens_to_ids(tgt_lang)
                                        
                                        import torch
                                        with torch.no_grad():
                                            outputs = nllb_model.generate(
                                                **inputs, 
                                                forced_bos_token_id=forced_bos, 
                                                max_length=512
                                            )
                                        translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
                                    
                                    if translated_text:
                                        print(f"Tłumaczenie ({gui.translate_lang}): {translated_text}")
                                        # Wstaw tylko przetłumaczony tekst
                                        word.insert_text(translated_text)
                                    else:
                                        print("⚠ Brak tłumaczenia - pomijam tekst")
                                        # NIE wstawiamy oryginału gdy tłumaczenie włączone
                                        
                                except Exception as e:
                                    print(f"⚠ Błąd tłumaczenia: {e}")
                                    print("Pomijam tekst - tłumaczenie nie powiodło się")
                                    # NIE wstawiamy oryginału gdy tłumaczenie włączone
                            else:
                                # Bez tłumaczenia - wstaw oryginalny tekst
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
