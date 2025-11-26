"""Test podstawowy - tworzenie i tłumaczenie prostego PDF"""
import fitz
from deep_translator import GoogleTranslator
import os

print("=== TEST 1: Tworzenie przykładowego PDF ===")

# Utwórz prosty PDF do testu
doc = fitz.open()
page = doc.new_page(width=595, height=842)  # A4

# Dodaj tekst
text = """To jest testowy dokument.
Zawiera kilka linii tekstu po polsku.
Ten dokument zostanie przetłumaczony na angielski.
Sprawdzamy czy tłumaczenie działa poprawnie."""

rect = fitz.Rect(50, 50, 545, 792)
page.insert_textbox(rect, text, fontsize=12, fontname="helv")

test_input = r"C:\Transkrybcja\traskryptor\test_input.pdf"
doc.save(test_input)
doc.close()
print(f"✓ Utworzono testowy PDF: {test_input}")

print("\n=== TEST 2: Tłumaczenie Google Translate ===")
try:
    translator = GoogleTranslator(source='pl', target='en')
    test_text = "Witaj świecie! To jest test tłumaczenia."
    translated = translator.translate(test_text)
    print(f"Oryginalny: {test_text}")
    print(f"Przetłumaczony: {translated}")
    
    if translated and "Hello" in translated or "world" in translated:
        print("✓ Tłumaczenie działa!")
    else:
        print(f"⚠ Tłumaczenie wygląda podejrzanie: {translated}")
except Exception as e:
    print(f"❌ Błąd tłumaczenia: {e}")
    import traceback
    traceback.print_exc()

print("\n=== TEST 3: Tłumaczenie PDF (prosty tryb) ===")
try:
    from pdf_translator import PDFTranslator
    
    translator = PDFTranslator(source_lang="pl", target_lang="en")
    output = r"C:\Transkrybcja\traskryptor\test_output_simple.pdf"
    
    success = translator.translate_pdf_simple(test_input, output)
    
    if success and os.path.exists(output):
        size = os.path.getsize(output)
        print(f"\n✓ SUKCES! Plik: {output}")
        print(f"✓ Rozmiar: {size} bajtów")
        
        # Sprawdź zawartość
        doc = fitz.open(output)
        text = doc[0].get_text()
        print(f"✓ Tekst w PDF ({len(text)} znaków):")
        print(text[:200])
        doc.close()
    else:
        print("❌ Tłumaczenie nie powiodło się")
except Exception as e:
    print(f"❌ Błąd: {e}")
    import traceback
    traceback.print_exc()
