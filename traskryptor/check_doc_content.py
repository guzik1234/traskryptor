"""Sprawdza pełną zawartość dokumentu"""
import win32com.client as win32
import sys

files_to_check = [
    r"c:\Transkrybcja\traskryptor\Podanie o uznanie wykonanej pracy jako praktyki z nazwiskiem dziekana.odt",
    r"c:\Transkrybcja\traskryptor\Podanie_FINAL_EN.docx"
]

for fpath in files_to_check:
    print("\n" + "="*80)
    print(f"PLIK: {fpath.split('\\')[-1]}")
    print("="*80)
    
    try:
        word = win32.Dispatch("Word.Application")
        word.Visible = False
        word.DisplayAlerts = 0
        
        doc = word.Documents.Open(fpath, ReadOnly=True)
        print(f"\nLiczba paragrafów: {doc.Paragraphs.Count}")
        print(f"Liczba stron: {doc.ComputeStatistics(2)}")
        print("\nZAWARTOŚĆ:")
        print("-"*80)
        
        for i in range(1, doc.Paragraphs.Count + 1):
            p = doc.Paragraphs.Item(i)
            text = p.Range.Text.rstrip("\r")
            if text.strip():  # Tylko niepuste
                print(f"{i:3}. {text[:100]}")
        
        doc.Close(SaveChanges=False)
        word.Quit()
        
    except Exception as e:
        print(f"BŁĄD: {e}")
        try:
            if 'doc' in locals():
                doc.Close(SaveChanges=False)
            if 'word' in locals():
                word.Quit()
        except:
            pass

print("\n" + "="*80)
print("KONIEC")
