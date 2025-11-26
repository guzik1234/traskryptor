"""Test Microsoft Word COM - diagnoza problemu"""
import os
import sys

print("="*60)
print("TEST 1: Import win32com")
print("="*60)
try:
    import win32com.client as win32
    print("✓ win32com zaimportowany")
except Exception as e:
    print(f"✗ BŁĄD importu: {e}")
    sys.exit(1)

print("\n" + "="*60)
print("TEST 2: Uruchomienie Microsoft Word")
print("="*60)
try:
    word = win32.Dispatch("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0
    print("✓ Word uruchomiony")
except Exception as e:
    print(f"✗ BŁĄD uruchamiania Word: {e}")
    sys.exit(1)

print("\n" + "="*60)
print("TEST 3: Otwieranie pliku ODT")
print("="*60)
odt_path = r"c:\Transkrybcja\traskryptor\Podanie o uznanie wykonanej pracy jako praktyki z nazwiskiem dziekana.odt"
if not os.path.exists(odt_path):
    print(f"✗ Plik nie istnieje: {odt_path}")
    word.Quit()
    sys.exit(1)

print(f"Plik: {os.path.basename(odt_path)}")
print(f"Rozmiar: {os.path.getsize(odt_path)} bajtów")

try:
    print("Otwieranie (może potrwać kilka sekund)...")
    doc = word.Documents.Open(odt_path, ReadOnly=True, ConfirmConversions=False)
    print(f"✓ Dokument otwarty")
    print(f"  Liczba stron: {doc.ComputeStatistics(2)}")  # wdStatisticPages
    print(f"  Liczba paragrafów: {doc.Paragraphs.Count}")
    
    # Pobierz pierwszy akapit
    if doc.Paragraphs.Count > 0:
        first_para = doc.Paragraphs.Item(1).Range.Text[:100]
        print(f"  Pierwszy akapit: '{first_para}'")
    
    doc.Close(SaveChanges=False)
    print("✓ Dokument zamknięty")
except Exception as e:
    print(f"✗ BŁĄD otwierania dokumentu: {e}")
    import traceback
    traceback.print_exc()
    word.Quit()
    sys.exit(1)

print("\n" + "="*60)
print("TEST 4: Zamykanie Word")
print("="*60)
try:
    word.Quit()
    print("✓ Word zamknięty")
except Exception as e:
    print(f"✗ BŁĄD zamykania: {e}")

print("\n" + "="*60)
print("✓✓✓ WSZYSTKIE TESTY ZAKOŃCZONE SUKCESEM ✓✓✓")
print("="*60)
