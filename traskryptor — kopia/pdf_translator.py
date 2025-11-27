import fitz  # PyMuPDF
from deep_translator import GoogleTranslator
import os
import re
import subprocess


class PDFTranslator:
    """Tłumaczy dokumenty PDF z polskiego na angielski lub rosyjski"""
    
    def __init__(self, source_lang="pl", target_lang="en"):
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.translator = GoogleTranslator(source=source_lang, target=target_lang)
        print(f"Translator zainicjalizowany: {source_lang} -> {target_lang}")
    
    def translate_text(self, text):
        """Tłumaczy pojedynczy fragment tekstu"""
        if not text or not text.strip():
            return text
        
        try:
            print(f"Tłumaczenie: {text[:50]}...")
            # deep-translator (Google Translate)
            translated = self.translator.translate(text)
            print(f"Wynik: {translated[:50] if translated else 'BRAK'}...")
            return translated if translated else text
        except Exception as e:
            print(f"Błąd tłumaczenia: {e}")
            import traceback
            traceback.print_exc()
            return text
    
    def translate_pdf(self, input_path, output_path, progress_callback=None):
        """
        Tłumaczy plik PDF zachowując szczegółowe formatowanie (tryb zaawansowany)
        TWORZY NOWY PDF bez oryginalnego tekstu
        """
        try:
            print(f"Otwieranie pliku: {input_path}")
            doc = fitz.open(input_path)
            total_pages = len(doc)
            print(f"Liczba stron: {total_pages}")
            
            # Utwórz nowy dokument
            output_doc = fitz.open()
            
            for page_num in range(total_pages):
                if progress_callback:
                    progress_callback(page_num + 1, total_pages)
                
                print(f"\n=== Strona {page_num + 1}/{total_pages} ===")
                page = doc[page_num]
                
                # Utwórz nową stronę
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
                
                # Dla każdego bloku tekstowego
                for block in blocks:
                    if block.get("type") == 0:  # Blok tekstowy
                        for line in block.get("lines", []):
                            for span in line.get("spans", []):
                                original_text = span.get("text", "")
                                
                                if not original_text.strip():
                                    continue
                                
                                # Pobierz pozycję i formatowanie
                                bbox = span["bbox"]
                                font_size = span.get("size", 11)
                                
                                # Tłumacz tekst
                                translated_text = self.translate_text(original_text)
                                
                                if not translated_text or not translated_text.strip():
                                    continue
                                
                                # Wstaw przetłumaczony tekst
                                rect = fitz.Rect(bbox)
                                
                                # Próbuj z coraz mniejszą czcionką aż się zmieści
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
                                    print(f"⚠ Nie zmieścił się: {translated_text[:30]}")
            
            print(f"\nZapisywanie do: {output_path}")
            output_doc.save(output_path, garbage=4, deflate=True)
            output_doc.close()
            doc.close()
            
            print("✓ Tłumaczenie zakończone!")
            return True
            
        except Exception as e:
            print(f"✗ Błąd: {e}")
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
        Prostsza wersja - tłumaczy PDF blok po bloku zachowując układ
        TWORZY NOWY PDF bez oryginalnego tekstu
        """
        try:
            print(f"Otwieranie pliku: {input_path}")
            doc = fitz.open(input_path)
            total_pages = len(doc)
            print(f"Liczba stron: {total_pages}")
            
            # Utwórz nowy dokument
            output_doc = fitz.open()
            
            for page_num in range(total_pages):
                if progress_callback:
                    progress_callback(page_num + 1, total_pages)
                
                print(f"\n=== Strona {page_num + 1}/{total_pages} ===")
                page = doc[page_num]
                
                # Pobierz bloki tekstu z formatowaniem (dict mode)
                page_dict = page.get_text("dict")
                blocks_simple = page.get_text("blocks")
                
                # Utwórz nową stronę (czysta, bez tekstu)
                new_page = output_doc.new_page(width=page.rect.width, height=page.rect.height)
                
                # Skopiuj obrazy i grafikę (bez tekstu)
                for block in page_dict["blocks"]:
                    if block.get("type") == 1:  # Obraz
                        try:
                            img_rect = fitz.Rect(block["bbox"])
                            pix = page.get_pixmap(clip=img_rect)
                            new_page.insert_image(img_rect, pixmap=pix)
                        except:
                            pass
                
                print(f"Bloków tekstowych: {len(blocks_simple)}")
                
                # Dla każdego bloku tekstowego - zachowaj dokładną pozycję i formatowanie
                for block_idx, block_data in enumerate(page_dict["blocks"]):
                    if block_data.get("type") != 0:  # Pomiń nie-tekstowe
                        continue
                    
                    # Zbierz tekst z całego bloku
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
                    
                    # Średni rozmiar czcionki w bloku
                    if fontsize_count > 0:
                        avg_fontsize = avg_fontsize / fontsize_count
                    else:
                        avg_fontsize = 10
                    
                    print(f"Blok {block_idx + 1} (font {avg_fontsize:.1f}pt): {full_text[:40]}...")
                    
                    # Tłumacz
                    translated = self.translate_text(full_text)
                    
                    if not translated or not translated.strip():
                        continue
                    
                    # Wstaw przetłumaczony tekst w DOKŁADNIE TYM SAMYM MIEJSCU
                    text_rect = fitz.Rect(bbox)
                    
                    # Oblicz szerokość prostokąta
                    rect_width = text_rect.width
                    page_width = new_page.rect.width
                    
                    # Określ wyrównanie na podstawie pozycji w PDF
                    if text_rect.x0 < page_width * 0.3:
                        align = 0  # Lewo
                    elif text_rect.x0 > page_width * 0.7:
                        align = 2  # Prawo
                    elif rect_width > page_width * 0.6:
                        align = 0  # Szerokie pole - lewo
                    else:
                        align = 1  # Środek
                    
                    # Próbuj z oryginalnym rozmiarem i mniejszymi
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
                            print(f"✓ Wstawiono ({fontsize:.1f}pt, align={align}): {translated[:30]}...")
                            inserted = True
                            break
                    
                    if not inserted:
                        print(f"⚠ Nie zmieścił się nawet z małą czcionką")
            
            print(f"\nZapisywanie do: {output_path}")
            output_doc.save(output_path, garbage=4, deflate=True)
            output_doc.close()
            doc.close()
            
            print("✓ Tłumaczenie zakończone pomyślnie!")
            return True
            
        except Exception as e:
            print(f"✗ Błąd podczas tłumaczenia PDF: {e}")
            import traceback
            traceback.print_exc()
            return False

    def translate_docx_to_docx_and_pdf(self, input_path, output_docx, output_pdf, progress_callback=None):
        """
        Tłumaczy plik Word (.docx) lub ODT (.odt), zapisuje jako DOCX i eksportuje do PDF.
        Zachowuje pełne formatowanie i układ dokumentu.
        """
        try:
            import win32com.client as win32
        except Exception as e:
            print(f"✗ Brak wsparcia COM / pywin32: {e}")
            return False

        word = None
        doc = None
        try:
            print("="*60)
            print(f"ROZPOCZYNAM TŁUMACZENIE")
            print(f"Plik wejściowy: {input_path}")
            print(f"DOCX wyjściowy: {output_docx}")
            print(f"PDF wyjściowy: {output_pdf}")
            print(f"Język: {self.source_lang} → {self.target_lang}")
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
                
                print("✓ Word uruchomiony")
            except Exception as e:
                print(f"✗ BŁĄD uruchamiania Word: {e}")
                raise

            print(f"\n[2/7] Otwieranie dokumentu: {os.path.basename(input_path)}")
            try:
                # Konwertuj na bezwzględną ścieżkę
                abs_path = os.path.abspath(input_path)
                print(f"Ścieżka bezwzględna: {abs_path}")
                
                # Sprawdź czy plik istnieje
                if not os.path.exists(abs_path):
                    raise FileNotFoundError(f"Plik nie istnieje: {abs_path}")
                
                # Otwórz dokument (Word automatycznie obsługuje ODT)
                doc = word.Documents.Open(abs_path, ReadOnly=False, ConfirmConversions=False)
                print(f"✓ Dokument otwarty")
            except Exception as e:
                print(f"✗ BŁĄD otwierania dokumentu: {e}")
                raise

            print(f"\n[3/7] Przygotowanie do tłumaczenia...")
            
            def should_skip_translation(s: str) -> bool:
                """Sprawdza czy tekst NIE powinien być tłumaczony (ale zachowany)."""
                t = s.strip()
                if not t:
                    return True  # Puste linie - zachowaj bez tłumaczenia
                # Sprawdź czy to linia składająca się TYLKO z kropek, kresek, spacji
                core = re.sub(r"[\s\.·•–—\-…_]+", "", t)
                if len(core) == 0:
                    return True  # Linia formularza - zachowaj bez tłumaczenia
                return False

            print(f"\n[4/7] Tłumaczenie zawartości dokumentu...")
            # Przetwarzaj główną treść i ramki tekstowe
            # Wartości: 1 = wdMainTextStory, 3 = wdTextFrameStory
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
                print(f"  Znaleziono akapitów: {count}")
                
                for i in range(1, count + 1):
                    p = paras.Item(i)
                    try:
                        original = p.Range.Text
                        trimmed = original.rstrip("\r")
                        
                        # Sprawdź czy pominąć tłumaczenie (ale zachować treść)
                        if should_skip_translation(trimmed):
                            # Zachowaj oryginalny tekst bez zmian (linie formularza, kropki itp.)
                            continue
                        
                        # Tłumacz
                        translated = self.translate_text(trimmed)
                        if not translated:
                            print(f"  ⚠ Brak tłumaczenia dla: '{trimmed[:50]}'")
                            continue
                        
                        p.Range.Text = translated + "\r"
                        total_translated += 1
                        
                        # Co 10 akapitów wypisz progress
                        if total_translated % 10 == 0:
                            print(f"  ✓ Przetłumaczono: {total_translated} akapitów")
                            
                    except Exception as e:
                        print(f"  ⚠ Błąd akapitu {i}: {e}")

            print(f"\n✓ Razem przetłumaczono: {total_translated} fragmentów")

            print(f"\n[5/7] Tłumaczenie kształtów (pola tekstowe)...")
            # Teksty w kształtach
            shapes_translated = 0
            try:
                shapes = doc.Shapes
                scount = shapes.Count if hasattr(shapes, 'Count') else 0
                print(f"  Znaleziono kształtów: {scount}")
                
                for si in range(1, scount + 1):
                    try:
                        sh = shapes.Item(si)
                        if hasattr(sh, 'TextFrame') and sh.TextFrame.HasText:
                            tr = sh.TextFrame.TextRange
                            txt = tr.Text.rstrip("\r")
                            
                            # Pomiń linie formularza, ale zachowaj je
                            if should_skip_translation(txt):
                                continue
                                
                            translated = self.translate_text(txt)
                            if translated:
                                tr.Text = translated + "\r"
                                shapes_translated += 1
                    except Exception as e:
                        print(f"  ⚠ Błąd shape {si}: {e}")
                        
                print(f"✓ Przetłumaczono kształtów: {shapes_translated}")
            except Exception as e:
                print(f"⚠ Błąd przetwarzania kształtów: {e}")

            print(f"\n[6/7] Zapisywanie plików...")
            # Zapisz jako DOCX
            print(f"  Zapisywanie DOCX: {os.path.basename(output_docx)}")
            try:
                abs_docx = os.path.abspath(output_docx)
                # FileFormat: 12 = wdFormatXMLDocument (DOCX)
                doc.SaveAs2(abs_docx, FileFormat=12)
                print(f"  ✓ DOCX zapisany")
            except Exception as e:
                print(f"  ✗ BŁĄD zapisu DOCX: {e}")
                raise

            # Eksportuj jako PDF
            print(f"  Eksportowanie PDF: {os.path.basename(output_pdf)}")
            try:
                abs_pdf = os.path.abspath(output_pdf)
                # ExportFormat: 17 = wdExportFormatPDF
                doc.ExportAsFixedFormat(OutputFileName=abs_pdf, ExportFormat=17)
                print(f"  ✓ PDF zapisany")
            except Exception as e:
                print(f"  ⚠ Błąd ExportAsFixedFormat: {e}")
                print(f"  Próbuję SaveAs2...")
                try:
                    # FileFormat: 17 = wdFormatPDF
                    doc.SaveAs2(abs_pdf, FileFormat=17)
                    print(f"  ✓ PDF zapisany (SaveAs2)")
                except Exception as e2:
                    print(f"  ✗ BŁĄD zapisu PDF: {e2}")
                    raise

            print(f"\n[7/7] Zamykanie dokumentu...")
            doc.Close(SaveChanges=False)
            word.Quit()
            print("✓ Word zamknięty")
            
            print("\n" + "="*60)
            print("✓✓✓ TŁUMACZENIE ZAKOŃCZONE SUKCESEM ✓✓✓")
            print("="*60)
            return True
            
        except Exception as e:
            print("\n" + "="*60)
            print(f"✗✗✗ BŁĄD KRYTYCZNY ✗✗✗")
            print(f"Typ błędu: {type(e).__name__}")
            print(f"Wiadomość: {e}")
            import traceback
            traceback.print_exc()
            print("="*60)
            
            # Sprzątanie przy błędzie
            try:
                if doc:
                    doc.Close(SaveChanges=False)
                    print("✓ Dokument zamknięty")
            except Exception:
                pass
            try:
                if word:
                    word.Quit()
                    print("✓ Word zamknięty")
            except Exception:
                pass
            
            return False

    def translate_pdf_via_word(self, input_path, output_path, progress_callback=None):
        """
        Konwersja PDF -> DOCX w Wordzie, tłumaczenie akapitów, eksport z powrotem do PDF.
        Najlepsza zgodność układu 1:1, wymaga zainstalowanego MS Word.
        """
        try:
            import win32com.client as win32
        except Exception as e:
            print(f"✗ Brak wsparcia COM / pywin32: {e}")
            return False

        try:
            print(f"Otwieranie w Wordzie: {input_path}")
            word = win32.Dispatch("Word.Application")
            word.Visible = False
            # 0 = wdAlertsNone
            word.DisplayAlerts = 0
            # Przyśpieszenie
            try:
                word.ScreenUpdating = False
            except Exception:
                pass

            # Przygotuj tymczasową kopię PDF (prosta nazwa)
            base, _ = os.path.splitext(output_path)
            temp_docx = base + "__tmp.docx"
            temp_pdf = base + "__tmp.pdf"
            try:
                import shutil
                shutil.copyfile(input_path, temp_pdf)
                input_for_word = temp_pdf
            except Exception:
                input_for_word = input_path

            # Spróbuj zdjąć blokadę Windows (Mark of the Web)
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

            # Otwórz PDF – bez potwierdzeń konwersji, spróbuj trybu NoRepairDialog
            try:
                doc = word.Documents.OpenNoRepairDialog(input_for_word, False, False)
            except Exception:
                doc = word.Documents.Open(input_for_word, ConfirmConversions=False, ReadOnly=False, AddToRecentFiles=False)

            # Zapisz jako tymczasowy DOCX, żeby utrwalić konwersję
            print(f"Zapisywanie konwersji do DOCX: {temp_docx}")
            # FileFormat: 12 = wdFormatXMLDocument (DOCX)
            doc.SaveAs2(temp_docx, FileFormat=12)

            # Tłumaczenie we wszystkich 'StoryRanges' (główna treść, ramki tekstowe, nagłówki itp.)
            def should_translate(s: str) -> bool:
                if not s:
                    return False
                t = s.strip().rstrip("\r")
                if not t:
                    return False
                # Pomiń linie z SAMYCH kropek / kresek / spacji (bez liter)
                core = re.sub(r"[\s\.·•–—\-…_]+", "", t)
                if len(core) == 0:
                    return False
                # Pomiń TYLKO pojedyncze znaki (np. "1", "-")
                if len(core) == 1 and not core.isalpha():
                    return False
                return True

            # Przetwarzaj szerzej: główna treść, ramki, nagłówki/stopki
            # Wartości stałych Word: 1=wdMainTextStory, 3=wdTextFrameStory, 5=wdPrimaryHeaderStory, 6=wdPrimaryFooterStory
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
                print(f"  Akapitów: {count}")
                for i in range(1, count + 1):
                    p = paras.Item(i)
                    try:
                        original = p.Range.Text
                        trimmed = original.rstrip("\r")
                        if not should_translate(trimmed):
                            print(f"  Pominięto: '{trimmed[:30]}'")
                            continue
                        print(f"  Tłumaczę: '{trimmed[:30]}'")
                        translated = self.translate_text(trimmed)
                        if not translated:
                            print(f"  Brak tłumaczenia dla: '{trimmed[:30]}'")
                            continue
                        p.Range.Text = translated + "\r"
                        print(f"  ✓ Zamieniono na: '{translated[:30]}'")
                    except Exception as e:
                        print(f"⚠ Błąd akapitu: {e}")

            # Teksty w kształtach (np. pola tekstowe poza StoryRanges)
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
                        print(f"⚠ Błąd shape: {e}")
            except Exception as e:
                print(f"⚠ Błąd shapes: {e}")

            # Zapis bezpośrednio do PDF – Word zachowuje układ
            print(f"Zapisywanie do PDF: {output_path}")
            try:
                # Preferowana metoda eksportu do PDF
                # ExportFormat: 17 = wdExportFormatPDF
                doc.ExportAsFixedFormat(OutputFileName=output_path, ExportFormat=17)
            except Exception:
                # Fallback do SaveAs2
                # FileFormat: 17 = wdFormatPDF
                doc.SaveAs2(output_path, FileFormat=17)

            # Sprzątanie
            doc.Close(SaveChanges=False)
            word.Quit()

            # Usuń pliki tymczasowe
            try:
                if os.path.exists(temp_docx):
                    os.remove(temp_docx)
                if os.path.exists(temp_pdf):
                    os.remove(temp_pdf)
            except Exception:
                pass

            print("✓ Tłumaczenie przez Word zakończone!")
            return True
        except Exception as e:
            print(f"✗ Błąd w translate_pdf_via_word: {e}")
            try:
                # Uporządkuj Worda przy błędzie
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
