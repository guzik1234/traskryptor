"""Test tłumaczenia PDF - pełny test z prawdziwym plikiem"""
from pdf_translator import PDFTranslator
import os

# Ścieżka do pliku
input_pdf = r"C:\Transkrybcja\traskryptor\Podanie o uznanie wykonanej pracy jako praktyki z nazwiskiem dziekana.pdf"
output_pdf = r"C:\Transkrybcja\traskryptor\test_translation_output.pdf"

print("=== TEST TŁUMACZENIA PDF ===\n")

# Sprawdź czy plik istnieje
if not os.path.exists(input_pdf):
    print(f"❌ Plik nie istnieje: {input_pdf}")
    exit(1)

print(f"✓ Plik znaleziony: {input_pdf}")

# Test tłumaczenia prostego
print("\n--- TEST 1: Tryb prosty ---")
try:
    translator = PDFTranslator(source_lang="pl", target_lang="en")
    
    def progress(current, total):
        print(f"Postęp: {current}/{total}")
    
    success = translator.translate_pdf_simple(input_pdf, output_pdf, progress_callback=progress)
    
    if success:
        print(f"\n✓ SUKCES! Plik zapisany: {output_pdf}")
        
        # Sprawdź czy plik został utworzony
        if os.path.exists(output_pdf):
            size = os.path.getsize(output_pdf)
            print(f"✓ Rozmiar pliku: {size} bajtów")
            
            if size > 1000:
                print("✓ Plik zawiera dane!")
            else:
                print("⚠ Plik jest bardzo mały - może być pusty")
        else:
            print("❌ Plik nie został utworzony")
    else:
        print("❌ Tłumaczenie nie powiodło się")
        
except Exception as e:
    print(f"❌ Błąd: {e}")
    import traceback
    traceback.print_exc()
