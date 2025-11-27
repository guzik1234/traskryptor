import fitz  # PyMuPDF
import os
import re
import subprocess

# Tryb offline – jeśli True używamy Argos Translate zamiast usług online.
# Tryb offline (bez połączeń z Internetem). Jeśli True używamy Argos Translate / HF NLLB fallback.
USE_OFFLINE = True

_offline_available = False
_hf_available = False
_argos_pairs = set()

if USE_OFFLINE:
    # Argos init + pary
    try:
        import argostranslate.translate as argos_translate
        _offline_available = True
        try:
            installed_langs = argos_translate.get_installed_languages()
            for src in installed_langs:
                for tgt in installed_langs:
                    _argos_pairs.add((src.code, tgt.code))
        except Exception:
            pass
    except ImportError:
        print("[OFFLINE] Brak pakietu argostranslate. Użyj: pip install argostranslate")
    # HF transformers fallback
    try:
        from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
        import torch
        _hf_available = True
    except ImportError:
        print("[FALLBACK] Brak transformers. Zainstaluj: pip install transformers")
else:
    try:
        from deep_translator import GoogleTranslator
    except ImportError:
        GoogleTranslator = None
        print("[ONLINE] deep_translator niedostępny.")


class PDFTranslator:
    """Tłumaczy dokumenty (Word/PDF) z polskiego na en/ru/uk.
    Priorytet: Argos offline -> HF NLLB fallback (ru/uk) -> Google online.
    """
    _hf_models = {}  # cache załadowanych modeli HF

    def __init__(self, source_lang="pl", target_lang="en"):
        self.source_lang = source_lang
        self.target_lang = target_lang
        if USE_OFFLINE:
            if _offline_available and (source_lang, target_lang) in _argos_pairs:
                print(f"[OFFLINE/ARGOS] {source_lang}->{target_lang}")
            elif target_lang in {"ru", "uk"} and _hf_available:
                print(f"[OFFLINE/FALLBACK HF] Ładowanie modelu NLLB dla {source_lang}->{target_lang}")
                self._load_hf_model(source_lang, target_lang)
            else:
                print(f"[OFFLINE WARN] Brak pary Argos i brak fallback dla {source_lang}->{target_lang}")
        else:
            if "GoogleTranslator" in globals() and GoogleTranslator:
                self.translator = GoogleTranslator(source=source_lang, target=target_lang)
                print(f"[ONLINE] GoogleTranslator: {source_lang} -> {target_lang}")
            else:
                print("[ERROR] Brak GoogleTranslator.")

    def _load_hf_model(self, src, tgt):
        pair = (src, tgt)
        if pair in self._hf_models:
            return
        model_name = "facebook/nllb-200-distilled-600M"
        try:
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
            lang_map = {"pl": "pol_Latn", "en": "eng_Latn", "ru": "rus_Cyrl", "uk": "ukr_Cyrl"}
            self._hf_models[pair] = (tokenizer, model, lang_map.get(src), lang_map.get(tgt))
            print(f"[HF/NLLB] Załadowano {model_name} dla {src}->{tgt}")
        except Exception as e:
            print(f"[HF ERR] Nie udało się załadować {model_name}: {e}")

    def _hf_translate(self, text):
        pair = (self.source_lang, self.target_lang)
        if pair not in self._hf_models:
            return text
        tokenizer, model, src_lang, tgt_lang = self._hf_models[pair]
        try:
            tokenizer.src_lang = src_lang
            inputs = tokenizer(text, return_tensors="pt", truncation=True)
            forced_bos = tokenizer.convert_tokens_to_ids(tgt_lang)
            with torch.no_grad():
                outputs = model.generate(**inputs, forced_bos_token_id=forced_bos, max_length=512)
            return tokenizer.decode(outputs[0], skip_special_tokens=True)
        except Exception as e:
            print(f"[HF GEN ERR] {e}")
            return text

    def _translate(self, text: str) -> str:
        if not text or not text.strip():
            return text
        if USE_OFFLINE:
            if _offline_available and (self.source_lang, self.target_lang) in _argos_pairs:
                try:
                    return argos_translate.translate(text, self.source_lang, self.target_lang)
                except Exception as e:
                    print(f"[ARGOS ERR] {e}")
            if self.target_lang in {"ru", "uk"} and _hf_available:
                return self._hf_translate(text)
            return text
        if hasattr(self, "translator"):
            try:
                return self.translator.translate(text)
            except Exception as e:
                print(f"[ONLINE ERR] {e}")
        return text

    def open_in_word(self, input_path):
        """Otwiera dokument w Microsoft Word (bez tłumaczenia)"""
        try:
            import win32com.client
            import pythoncom
            
            pythoncom.CoInitialize()
            word = win32com.client.Dispatch("Word.Application")
            word.Visible = True
            
            abs_input = os.path.abspath(input_path)
            print(f"Otwieranie w Word: {abs_input}")
            
            doc = word.Documents.Open(abs_input)
            print(f" Dokument otwarty w Word: {os.path.basename(abs_input)}")
            
            # Nie zamykamy - użytkownik może sprawdzić dokument
            return True
            
        except Exception as e:
            print(f"Błąd otwierania w Word: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def translate_text(self, text):
        if not text or not text.strip():
            return text
        print(f"Tłumaczenie: {text[:50]}...")
        translated = self._translate(text)
        print(f"Wynik: {translated[:50] if translated else 'BRAK'}...")
        return translated if translated else text
    
    def translate_pdf(self, input_path, output_path, progress_callback=None):
        """
        TĹ‚umaczy plik PDF zachowujÄ…c szczegĂłĹ‚owe formatowanie (tryb zaawansowany)
        TWORZY NOWY PDF bez oryginalnego tekstu
        """
        try:
            print(f"Otwieranie pliku: {input_path}")
            doc = fitz.open(input_path)
            total_pages = len(doc)
            print(f"Liczba stron: {total_pages}")
            
            # UtwĂłrz nowy dokument
            output_doc = fitz.open()
            
            for page_num in range(total_pages):
                if progress_callback:
                    progress_callback(page_num + 1, total_pages)
                
                print(f"\n=== Strona {page_num + 1}/{total_pages} ===")
                page = doc[page_num]
                
                # UtwĂłrz nowÄ… stronÄ™
                new_page = output_doc.new_page(width=page.rect.width, height=page.rect.height)
                
                # Skopiuj obrazy
                page_dict = page.get_text("dict")
                for block in page_dict["blocks"]:
                    if block.get("type") == 1:  # Obraz
                        try:
                            img_rect = fitz.Rect(block["bbox"])
                            pix = page.get_pixmap(clip=img_rect)
                            new_page.insert_image(img_rect, pixmap=pix)
                        except:
                            pass
                
                # Pobierz bloki tekstu z pozycjami
                blocks = page_dict["blocks"]
                
                # Dla kaĹĽdego bloku tekstowego
                for block in blocks:
                    if block.get("type") == 0:  # Blok tekstowy
                        for line in block.get("lines", []):
                            for span in line.get("spans", []):
                                original_text = span.get("text", "")
                                
                                if not original_text.strip():
                                    continue
                                
                                # Pobierz pozycjÄ™ i formatowanie
                                bbox = span["bbox"]
                                font_size = span.get("size", 11)
                                
                                # TĹ‚umacz tekst
                                translated_text = self.translate_text(original_text)
                                
                                if not translated_text or not translated_text.strip():
                                    continue
                                
                                # Wstaw przetĹ‚umaczony tekst
                                rect = fitz.Rect(bbox)
                                
                                # PrĂłbuj z coraz mniejszÄ… czcionkÄ… aĹĽ siÄ™ zmieĹ›ci
                                inserted = False
                                for fontsize in [font_size, font_size * 0.8, font_size * 0.6, 8, 6, 5]:
                                    rc = new_page.insert_textbox(
                                        rect,
                                        translated_text,
                                        fontsize=fontsize,
                                        fontname="helv",
                                        color=(0, 0, 0),
                                        align=0
                                    )
                                    
                                    if rc >= 0:
                                        inserted = True
                                        break
                                
                                if not inserted:
                                    print(f"âš  Nie zmieĹ›ciĹ‚ siÄ™: {translated_text[:30]}")
            
            print(f"\nZapisywanie do: {output_path}")
            output_doc.save(output_path, garbage=4, deflate=True)
            output_doc.close()
            doc.close()
            
            print("âś“ TĹ‚umaczenie zakoĹ„czone!")
            return True
            
        except Exception as e:
            print(f"âś— BĹ‚Ä…d: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _int_to_rgb(self, color_int):
        """Konwertuje kolor z int na tuple RGB"""
        if color_int == 0:
            return (0, 0, 0)  # Czarny
        
        # Konwersja z formatu integer na RGB
        b = color_int & 0xFF
        g = (color_int >> 8) & 0xFF
        r = (color_int >> 16) & 0xFF
        
        return (r/255.0, g/255.0, b/255.0)
    
    def translate_pdf_simple(self, input_path, output_path, progress_callback=None):
        """
        Prostsza wersja - tĹ‚umaczy PDF blok po bloku zachowujÄ…c ukĹ‚ad
        TWORZY NOWY PDF bez oryginalnego tekstu
        """
        try:
            print(f"Otwieranie pliku: {input_path}")
            doc = fitz.open(input_path)
            total_pages = len(doc)
            print(f"Liczba stron: {total_pages}")
            
            # UtwĂłrz nowy dokument
            output_doc = fitz.open()
            
            for page_num in range(total_pages):
                if progress_callback:
                    progress_callback(page_num + 1, total_pages)
                
                print(f"\n=== Strona {page_num + 1}/{total_pages} ===")
                page = doc[page_num]
                
                # Pobierz bloki tekstu z formatowaniem (dict mode)
                page_dict = page.get_text("dict")
                blocks_simple = page.get_text("blocks")
                
                # UtwĂłrz nowÄ… stronÄ™ (czysta, bez tekstu)
                new_page = output_doc.new_page(width=page.rect.width, height=page.rect.height)
                
                # Skopiuj obrazy i grafikÄ™ (bez tekstu)
                for block in page_dict["blocks"]:
                    if block.get("type") == 1:  # Obraz
                        try:
                            img_rect = fitz.Rect(block["bbox"])
                            pix = page.get_pixmap(clip=img_rect)
                            new_page.insert_image(img_rect, pixmap=pix)
                        except:
                            pass
                
                print(f"BlokĂłw tekstowych: {len(blocks_simple)}")
                
                # Dla kaĹĽdego bloku tekstowego - zachowaj dokĹ‚adnÄ… pozycjÄ™ i formatowanie
                for block_idx, block_data in enumerate(page_dict["blocks"]):
                    if block_data.get("type") != 0:  # PomiĹ„ nie-tekstowe
                        continue
                    
                    # Zbierz tekst z caĹ‚ego bloku
                    bbox = block_data["bbox"]
                    full_text = ""
                    avg_fontsize = 0
                    fontsize_count = 0
                    
                    for line in block_data.get("lines", []):
                        for span in line.get("spans", []):
                            full_text += span.get("text", "")
                            fsize = span.get("size", 10)
                            avg_fontsize += fsize
                            fontsize_count += 1
                    
                    full_text = full_text.strip()
                    if not full_text:
                        continue
                    
                    # Ĺšredni rozmiar czcionki w bloku
                    if fontsize_count > 0:
                        avg_fontsize = avg_fontsize / fontsize_count
                    else:
                        avg_fontsize = 10
                    
                    print(f"Blok {block_idx + 1} (font {avg_fontsize:.1f}pt): {full_text[:40]}...")
                    
                    # TĹ‚umacz
                    translated = self.translate_text(full_text)
                    
                    if not translated or not translated.strip():
                        continue
                    
                    # Wstaw przetĹ‚umaczony tekst w DOKĹADNIE TYM SAMYM MIEJSCU
                    text_rect = fitz.Rect(bbox)
                    
                    # Oblicz szerokoĹ›Ä‡ prostokÄ…ta
                    rect_width = text_rect.width
                    page_width = new_page.rect.width
                    
                    # OkreĹ›l wyrĂłwnanie na podstawie pozycji w PDF
                    if text_rect.x0 < page_width * 0.3:
                        align = 0  # Lewo
                    elif text_rect.x0 > page_width * 0.7:
                        align = 2  # Prawo
                    elif rect_width > page_width * 0.6:
                        align = 0  # Szerokie pole - lewo
                    else:
                        align = 1  # Ĺšrodek
                    
                    # PrĂłbuj z oryginalnym rozmiarem i mniejszymi
                    inserted = False
                    for fontsize in [avg_fontsize, avg_fontsize * 0.9, avg_fontsize * 0.8, 8, 6, 5]:
                        rc = new_page.insert_textbox(
                            text_rect,
                            translated,
                            fontsize=fontsize,
                            fontname="helv",
                            color=(0, 0, 0),
                            align=align
                        )
                        
                        if rc >= 0:
                            print(f"âś“ Wstawiono ({fontsize:.1f}pt, align={align}): {translated[:30]}...")
                            inserted = True
                            break
                    
                    if not inserted:
                        print(f"âš  Nie zmieĹ›ciĹ‚ siÄ™ nawet z maĹ‚Ä… czcionkÄ…")
            
            print(f"\nZapisywanie do: {output_path}")
            output_doc.save(output_path, garbage=4, deflate=True)
            output_doc.close()
            doc.close()
            
            print("âś“ TĹ‚umaczenie zakoĹ„czone pomyĹ›lnie!")
            return True
            
        except Exception as e:
            print(f"âś— BĹ‚Ä…d podczas tĹ‚umaczenia PDF: {e}")
            import traceback
            traceback.print_exc()
            return False

    def translate_docx_to_docx_and_pdf(self, input_path, output_docx, output_pdf, progress_callback=None):
        """
        TĹ‚umaczy plik Word (.docx) lub ODT (.odt), zapisuje jako DOCX i eksportuje do PDF.
        Zachowuje peĹ‚ne formatowanie i ukĹ‚ad dokumentu.
        """
        try:
            import win32com.client as win32
        except Exception as e:
            print(f"âś— Brak wsparcia COM / pywin32: {e}")
            return False

        word = None
        doc = None
        try:
            print("="*60)
            print(f"ROZPOCZYNAM TĹUMACZENIE")
            print(f"Plik wejĹ›ciowy: {input_path}")
            print(f"DOCX wyjĹ›ciowy: {output_docx}")
            print(f"PDF wyjĹ›ciowy: {output_pdf}")
            print(f"JÄ™zyk: {self.source_lang} â†’ {self.target_lang}")
            print("="*60)

            print(f"\n[1/7] Uruchamianie Microsoft Word...")
            try:
                word = win32.Dispatch("Word.Application")
                word.Visible = False
                word.DisplayAlerts = 0
                
                try:
                    word.ScreenUpdating = False
                except Exception:
                    pass
                
                print("âś“ Word uruchomiony")
            except Exception as e:
                print(f"âś— BĹÄ„D uruchamiania Word: {e}")
                raise

            print(f"\n[2/7] Otwieranie dokumentu: {os.path.basename(input_path)}")
            try:
                # Konwertuj na bezwzglÄ™dnÄ… Ĺ›cieĹĽkÄ™
                abs_path = os.path.abspath(input_path)
                print(f"ĹšcieĹĽka bezwzglÄ™dna: {abs_path}")
                
                # SprawdĹş czy plik istnieje
                if not os.path.exists(abs_path):
                    raise FileNotFoundError(f"Plik nie istnieje: {abs_path}")
                
                # OtwĂłrz dokument (Word automatycznie obsĹ‚uguje ODT)
                doc = word.Documents.Open(abs_path, ReadOnly=False, ConfirmConversions=False)
                print(f"âś“ Dokument otwarty")
            except Exception as e:
                print(f"âś— BĹÄ„D otwierania dokumentu: {e}")
                raise

            print(f"\n[3/7] Przygotowanie do tĹ‚umaczenia...")
            
            def should_skip_translation(s: str) -> bool:
                """Sprawdza czy tekst NIE powinien byÄ‡ tĹ‚umaczony (ale ZAWSZE zachowany 1:1)."""
                t = s.strip()
                if not t:
                    return True  # Tylko caĹ‚kowicie puste linie
                # JeĹ›li jest JAKAKOLWIEK litera lub cyfra - tĹ‚umacz
                if re.search(r'[a-zA-ZÄ…Ä‡Ä™Ĺ‚Ĺ„ĂłĹ›ĹşĹĽÄ„Ä†ÄĹĹĂ“ĹšĹąĹ»0-9]', t):
                    return False  # Ma treĹ›Ä‡ do tĹ‚umaczenia
                # JeĹ›li to TYLKO znaki specjalne (kropki, kreski) - nie tĹ‚umacz, ale zachowaj
                return True

            print(f"\n[4/7] TĹ‚umaczenie zawartoĹ›ci dokumentu...")
            # Przetwarzaj gĹ‚ĂłwnÄ… treĹ›Ä‡ i ramki tekstowe
            # WartoĹ›ci: 1 = wdMainTextStory, 3 = wdTextFrameStory
            story_types = [
                1,  # wdMainTextStory
                3,  # wdTextFrameStory
            ]

            total_translated = 0
            for stype in story_types:
                try:
                    rng = doc.StoryRanges(stype)
                except Exception:
                    rng = None
                if not rng:
                    continue

                print(f"\nPrzetwarzanie story typu: {stype}")
                paras = rng.Paragraphs
                count = paras.Count if hasattr(paras, "Count") else 0
                print(f"  Znaleziono akapitĂłw: {count}")
                
                for i in range(1, count + 1):
                    p = paras.Item(i)
                    try:
                        original = p.Range.Text
                        trimmed = original.rstrip("\r")
                        
                        # SprawdĹş czy pominÄ…Ä‡ tĹ‚umaczenie (ale zachowaÄ‡ treĹ›Ä‡)
                        if should_skip_translation(trimmed):
                            # Zachowaj oryginalny tekst bez zmian (linie formularza, kropki itp.)
                            continue
                        
                        # Zachowaj oryginalne formatowanie (tabulatory, spacje na poczÄ…tku/koĹ„cu)
                        leading_spaces = len(original) - len(original.lstrip(' \t'))
                        trailing_spaces = len(original.rstrip("\r")) - len(original.rstrip("\r").rstrip(' \t'))
                        
                        # TĹ‚umacz tylko Ĺ›rodkowÄ… czÄ™Ĺ›Ä‡
                        core_text = original.lstrip(' \t').rstrip("\r").rstrip(' \t')
                        
                        if not core_text.strip():
                            continue
                        
                        translated = self.translate_text(core_text)
                        if not translated:
                            print(f"  âš  Brak tĹ‚umaczenia dla: '{core_text[:50]}'")
                            continue
                        
                        # OdtwĂłrz z oryginalnym formatowaniem
                        leading = original[:leading_spaces]
                        trailing = original[len(original.rstrip("\r")) - trailing_spaces:len(original.rstrip("\r"))]
                        p.Range.Text = leading + translated + trailing + "\r"
                        total_translated += 1
                        
                        # Co 10 akapitĂłw wypisz progress
                        if total_translated % 10 == 0:
                            print(f"  âś“ PrzetĹ‚umaczono: {total_translated} akapitĂłw")
                            
                    except Exception as e:
                        print(f"  âš  BĹ‚Ä…d akapitu {i}: {e}")

            print(f"\nâś“ Razem przetĹ‚umaczono: {total_translated} fragmentĂłw")

            print(f"\n[5/7] TĹ‚umaczenie ksztaĹ‚tĂłw (pola tekstowe)...")
            # Teksty w ksztaĹ‚tach
            shapes_translated = 0
            try:
                shapes = doc.Shapes
                scount = shapes.Count if hasattr(shapes, 'Count') else 0
                print(f"  Znaleziono ksztaĹ‚tĂłw: {scount}")
                
                for si in range(1, scount + 1):
                    try:
                        sh = shapes.Item(si)
                        if hasattr(sh, 'TextFrame') and sh.TextFrame.HasText:
                            tr = sh.TextFrame.TextRange
                            txt = tr.Text.rstrip("\r")
                            
                            # PomiĹ„ linie formularza, ale zachowaj je
                            if should_skip_translation(txt):
                                continue
                                
                            translated = self.translate_text(txt)
                            if translated:
                                tr.Text = translated + "\r"
                                shapes_translated += 1
                    except Exception as e:
                        print(f"  âš  BĹ‚Ä…d shape {si}: {e}")
                        
                print(f"âś“ PrzetĹ‚umaczono ksztaĹ‚tĂłw: {shapes_translated}")
            except Exception as e:
                print(f"âš  BĹ‚Ä…d przetwarzania ksztaĹ‚tĂłw: {e}")

            print(f"\n[6/7] Zapisywanie plikĂłw...")
            # Zapisz jako DOCX
            print(f"  Zapisywanie DOCX: {os.path.basename(output_docx)}")
            try:
                abs_docx = os.path.abspath(output_docx)
                # FileFormat: 12 = wdFormatXMLDocument (DOCX)
                doc.SaveAs2(abs_docx, FileFormat=12)
                print(f"  âś“ DOCX zapisany")
            except Exception as e:
                print(f"  âś— BĹÄ„D zapisu DOCX: {e}")
                raise

            # Eksportuj jako PDF
            print(f"  Eksportowanie PDF: {os.path.basename(output_pdf)}")
            try:
                abs_pdf = os.path.abspath(output_pdf)
                # ExportFormat: 17 = wdExportFormatPDF
                doc.ExportAsFixedFormat(OutputFileName=abs_pdf, ExportFormat=17)
                print(f"  âś“ PDF zapisany")
            except Exception as e:
                print(f"  âš  BĹ‚Ä…d ExportAsFixedFormat: {e}")
                print(f"  PrĂłbujÄ™ SaveAs2...")
                try:
                    # FileFormat: 17 = wdFormatPDF
                    doc.SaveAs2(abs_pdf, FileFormat=17)
                    print(f"  âś“ PDF zapisany (SaveAs2)")
                except Exception as e2:
                    print(f"  âś— BĹÄ„D zapisu PDF: {e2}")
                    raise

            print(f"\n[7/7] Zamykanie dokumentu...")
            doc.Close(SaveChanges=False)
            word.Quit()
            print("âś“ Word zamkniÄ™ty")
            
            print("\n" + "="*60)
            print("âś“âś“âś“ TĹUMACZENIE ZAKOĹCZONE SUKCESEM âś“âś“âś“")
            print("="*60)
            return True
            
        except Exception as e:
            print("\n" + "="*60)
            print(f"âś—âś—âś— BĹÄ„D KRYTYCZNY âś—âś—âś—")
            print(f"Typ bĹ‚Ä™du: {type(e).__name__}")
            print(f"WiadomoĹ›Ä‡: {e}")
            import traceback
            traceback.print_exc()
            print("="*60)
            
            # SprzÄ…tanie przy bĹ‚Ä™dzie
            try:
                if doc:
                    doc.Close(SaveChanges=False)
                    print("âś“ Dokument zamkniÄ™ty")
            except Exception:
                pass
            try:
                if word:
                    word.Quit()
                    print("âś“ Word zamkniÄ™ty")
            except Exception:
                pass
            
            return False

    def translate_pdf_via_word(self, input_path, output_path, progress_callback=None):
        """
        Konwersja PDF -> DOCX w Wordzie, tĹ‚umaczenie akapitĂłw, eksport z powrotem do PDF.
        Najlepsza zgodnoĹ›Ä‡ ukĹ‚adu 1:1, wymaga zainstalowanego MS Word.
        """
        try:
            import win32com.client as win32
        except Exception as e:
            print(f"âś— Brak wsparcia COM / pywin32: {e}")
            return False

        try:
            print(f"Otwieranie w Wordzie: {input_path}")
            word = win32.Dispatch("Word.Application")
            word.Visible = False
            # 0 = wdAlertsNone
            word.DisplayAlerts = 0
            # PrzyĹ›pieszenie
            try:
                word.ScreenUpdating = False
            except Exception:
                pass

            # Przygotuj tymczasowÄ… kopiÄ™ PDF (prosta nazwa)
            base, _ = os.path.splitext(output_path)
            temp_docx = base + "__tmp.docx"
            temp_pdf = base + "__tmp.pdf"
            try:
                import shutil
                shutil.copyfile(input_path, temp_pdf)
                input_for_word = temp_pdf
            except Exception:
                input_for_word = input_path

            # SprĂłbuj zdjÄ…Ä‡ blokadÄ™ Windows (Mark of the Web)
            try:
                if os.name == 'nt':
                    subprocess.run([
                        'powershell',
                        '-NoProfile',
                        '-Command',
                        f"Unblock-File -Path '{input_for_word}'"
                    ], capture_output=True, text=True)
            except Exception:
                pass

            # OtwĂłrz PDF â€“ bez potwierdzeĹ„ konwersji, sprĂłbuj trybu NoRepairDialog
            try:
                doc = word.Documents.OpenNoRepairDialog(input_for_word, False, False)
            except Exception:
                doc = word.Documents.Open(input_for_word, ConfirmConversions=False, ReadOnly=False, AddToRecentFiles=False)

            # Zapisz jako tymczasowy DOCX, ĹĽeby utrwaliÄ‡ konwersjÄ™
            print(f"Zapisywanie konwersji do DOCX: {temp_docx}")
            # FileFormat: 12 = wdFormatXMLDocument (DOCX)
            doc.SaveAs2(temp_docx, FileFormat=12)

            # TĹ‚umaczenie we wszystkich 'StoryRanges' (gĹ‚Ăłwna treĹ›Ä‡, ramki tekstowe, nagĹ‚Ăłwki itp.)
            def should_translate(s: str) -> bool:
                if not s:
                    return False
                t = s.strip().rstrip("\r")
                if not t:
                    return False
                # PomiĹ„ linie z SAMYCH kropek / kresek / spacji (bez liter)
                core = re.sub(r"[\s\.Â·â€˘â€“â€”\-â€¦_]+", "", t)
                if len(core) == 0:
                    return False
                # PomiĹ„ TYLKO pojedyncze znaki (np. "1", "-")
                if len(core) == 1 and not core.isalpha():
                    return False
                return True

            # Przetwarzaj szerzej: gĹ‚Ăłwna treĹ›Ä‡, ramki, nagĹ‚Ăłwki/stopki
            # WartoĹ›ci staĹ‚ych Word: 1=wdMainTextStory, 3=wdTextFrameStory, 5=wdPrimaryHeaderStory, 6=wdPrimaryFooterStory
            story_types = [
                1,  # wdMainTextStory
                3,  # wdTextFrameStory
                5,  # wdPrimaryHeaderStory
                6,  # wdPrimaryFooterStory
                8,  # wdEvenPagesHeaderStory
                9,  # wdEvenPagesFooterStory
                10, # wdFirstPageHeaderStory
                11, # wdFirstPageFooterStory
            ]

            for stype in story_types:
                try:
                    rng = doc.StoryRanges(stype)
                except Exception:
                    rng = None
                if not rng:
                    continue

                print(f"Przetwarzanie story: {stype}")
                paras = rng.Paragraphs
                count = paras.Count if hasattr(paras, "Count") else 0
                print(f"  AkapitĂłw: {count}")
                for i in range(1, count + 1):
                    p = paras.Item(i)
                    try:
                        original = p.Range.Text
                        trimmed = original.rstrip("\r")
                        if not should_translate(trimmed):
                            print(f"  PominiÄ™to: '{trimmed[:30]}'")
                            continue
                        print(f"  TĹ‚umaczÄ™: '{trimmed[:30]}'")
                        translated = self.translate_text(trimmed)
                        if not translated:
                            print(f"  Brak tĹ‚umaczenia dla: '{trimmed[:30]}'")
                            continue
                        p.Range.Text = translated + "\r"
                        print(f"  âś“ Zamieniono na: '{translated[:30]}'")
                    except Exception as e:
                        print(f"âš  BĹ‚Ä…d akapitu: {e}")

            # Teksty w ksztaĹ‚tach (np. pola tekstowe poza StoryRanges)
            try:
                shapes = doc.Shapes
                scount = shapes.Count if hasattr(shapes, 'Count') else 0
                for si in range(1, scount + 1):
                    try:
                        sh = shapes.Item(si)
                        if hasattr(sh, 'TextFrame') and sh.TextFrame.HasText:
                            tr = sh.TextFrame.TextRange
                            txt = tr.Text.rstrip("\r")
                            if should_translate(txt):
                                tr.Text = (self.translate_text(txt) or txt) + "\r"
                    except Exception as e:
                        print(f"âš  BĹ‚Ä…d shape: {e}")
            except Exception as e:
                print(f"âš  BĹ‚Ä…d shapes: {e}")

            # Zapis bezpoĹ›rednio do PDF â€“ Word zachowuje ukĹ‚ad
            print(f"Zapisywanie do PDF: {output_path}")
            try:
                # Preferowana metoda eksportu do PDF
                # ExportFormat: 17 = wdExportFormatPDF
                doc.ExportAsFixedFormat(OutputFileName=output_path, ExportFormat=17)
            except Exception:
                # Fallback do SaveAs2
                # FileFormat: 17 = wdFormatPDF
                doc.SaveAs2(output_path, FileFormat=17)

            # SprzÄ…tanie
            doc.Close(SaveChanges=False)
            word.Quit()

            # UsuĹ„ pliki tymczasowe
            try:
                if os.path.exists(temp_docx):
                    os.remove(temp_docx)
                if os.path.exists(temp_pdf):
                    os.remove(temp_pdf)
            except Exception:
                pass

            print("âś“ TĹ‚umaczenie przez Word zakoĹ„czone!")
            return True
        except Exception as e:
            print(f"âś— BĹ‚Ä…d w translate_pdf_via_word: {e}")
            try:
                # UporzÄ…dkuj Worda przy bĹ‚Ä™dzie
                doc.Close(SaveChanges=False)
            except Exception:
                pass
            try:
                word.Quit()
            except Exception:
                pass
            import traceback
            traceback.print_exc()
            return False

