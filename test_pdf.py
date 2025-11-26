"""Test PDF - sprawdza czy PDF jest poprawnie odczytywany i tłumaczony"""
import fitz
from deep_translator import GoogleTranslator

# Test 1: Odczyt PDF
print("=== TEST 1: Odczyt PDF ===")
pdf_path = r"C:\Transkrybcja\traskryptor\Podanie o uznanie wykonanej pracy jako praktyki z nazwiskiem dziekana.pdf"

try:
    doc = fitz.open(pdf_path)
    print(f"✓ PDF otwarty: {len(doc)} stron")
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        print(f"\n--- Strona {page_num + 1} ---")
        print(f"Długość tekstu: {len(text)} znaków")
        print(f"Pierwsze 200 znaków:\n{text[:200]}")
    
    doc.close()
except Exception as e:
    print(f"✗ Błąd: {e}")
    import traceback
    traceback.print_exc()

# Test 2: Tłumaczenie
print("\n\n=== TEST 2: Tłumaczenie ===")
try:
    translator = GoogleTranslator(source='pl', target='en')
    test_text = "Witaj świecie! To jest test."
    translated = translator.translate(test_text)
    print(f"Oryginalny: {test_text}")
    print(f"Przetłumaczony: {translated}")
    
    if translated and translated != test_text:
        print("✓ Tłumaczenie działa!")
    else:
        print("✗ Tłumaczenie nie działa!")
except Exception as e:
    print(f"✗ Błąd: {e}")
    import traceback
    traceback.print_exc()

# Test 3: Tworzenie PDF
print("\n\n=== TEST 3: Tworzenie PDF ===")
try:
    output = fitz.open()
    new_page = output.new_page(width=595, height=842)  # A4
    
    test_text = "This is a test document.\nSecond line here."
    rect = fitz.Rect(50, 50, 545, 792)
    
    rc = new_page.insert_textbox(
        rect,
        test_text,
        fontsize=11,
        fontname="helv",
        color=(0, 0, 0),
        align=0
    )
    
    print(f"insert_textbox return code: {rc}")
    
    if rc >= 0:
        print("✓ Tekst wstawiony pomyślnie")
    else:
        print("✗ Błąd wstawiania tekstu")
    
    test_output = r"C:\Transkrybcja\traskryptor\test_output.pdf"
    output.save(test_output)
    output.close()
    print(f"✓ Zapisano test PDF: {test_output}")
    
except Exception as e:
    print(f"✗ Błąd: {e}")
    import traceback
    traceback.print_exc()
