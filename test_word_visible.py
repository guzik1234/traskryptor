"""Test z WIDOCZNYM Word - aby zobaczyć co się dzieje"""
import os
import sys
import time

print("Test Word COM z WIDOCZNYM oknem")
print("="*60)

try:
    import win32com.client as win32
    print("✓ win32com zaimportowany")
except Exception as e:
    print(f"✗ BŁĄD: {e}")
    sys.exit(1)

odt_path = r"c:\Transkrybcja\traskryptor\Podanie o uznanie wykonanej pracy jako praktyki z nazwiskiem dziekana.odt"

print(f"\nPlik: {os.path.basename(odt_path)}")
print(f"Istnieje: {os.path.exists(odt_path)}")

print("\nUruchamianie Word (WIDOCZNY)...")
try:
    word = win32.Dispatch("Word.Application")
    word.Visible = True  # WIDOCZNY!
    word.DisplayAlerts = 0
    print("✓ Word uruchomiony")
    print("\n⚠ SPRAWDŹ CZY WORD WYŚWIETLA JAKIEŚ DIALOGI!")
    print("⚠ Jeśli widoczny jest dialog 'Protected View' - kliknij 'Enable Editing'")
    time.sleep(2)
except Exception as e:
    print(f"✗ BŁĄD: {e}")
    sys.exit(1)

print("\nOtwieranie dokumentu...")
print("(Może pojawić się dialog z prośbą o potwierdzenie konwersji ODT)")
try:
    doc = word.Documents.Open(odt_path, ReadOnly=False, ConfirmConversions=False)
    print(f"✓ Dokument otwarty")
    
    print("\nCzekam 5 sekund - SPRAWDŹ OKNO WORD...")
    time.sleep(5)
    
    print(f"\nLiczba paragrafów: {doc.Paragraphs.Count}")
    if doc.Paragraphs.Count > 0:
        first_text = doc.Paragraphs.Item(1).Range.Text[:100]
        print(f"Pierwszy akapit: '{first_text}'")
    
    print("\nZamykanie dokumentu...")
    doc.Close(SaveChanges=False)
    print("✓ Dokument zamknięty")
    
except Exception as e:
    print(f"✗ BŁĄD: {e}")
    import traceback
    traceback.print_exc()

print("\nZamykanie Word...")
try:
    word.Quit()
    print("✓ Word zamknięty")
except Exception:
    pass

print("\n" + "="*60)
print("Test zakończony")
