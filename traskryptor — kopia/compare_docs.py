"""Porównuje liczbę paragrafów i ich treść"""
import win32com.client as win32

print("Sprawdzanie oryginalnego dokumentu...")
word = win32.Dispatch("Word.Application")
word.Visible = False

# Oryginalny
doc1 = word.Documents.Open(r"c:\Transkrybcja\traskryptor\Podanie o uznanie wykonanej pracy jako praktyki z nazwiskiem dziekana.odt", ReadOnly=True)
print(f"ORYGINALNY ODT - Paragrafy: {doc1.Paragraphs.Count}")

original_paras = []
for i in range(1, doc1.Paragraphs.Count + 1):
    text = doc1.Paragraphs.Item(i).Range.Text.rstrip("\r")
    original_paras.append(text)
    if text.strip():
        print(f"  {i}: {text[:70]}")

doc1.Close(False)

print("\n" + "="*80)
print("Sprawdzanie przetłumaczonego dokumentu...")

# Przetłumaczony
doc2 = word.Documents.Open(r"c:\Transkrybcja\traskryptor\Podanie_FINAL_EN.docx", ReadOnly=True)
print(f"PRZETŁUMACZONY DOCX - Paragrafy: {doc2.Paragraphs.Count}")

translated_paras = []
for i in range(1, doc2.Paragraphs.Count + 1):
    text = doc2.Paragraphs.Item(i).Range.Text.rstrip("\r")
    translated_paras.append(text)
    if text.strip():
        print(f"  {i}: {text[:70]}")

doc2.Close(False)
word.Quit()

print("\n" + "="*80)
print(f"RÓŻNICA: {len(original_paras)} vs {len(translated_paras)} paragrafów")

# Pokaż co zginęło
missing = []
for idx, orig in enumerate(original_paras):
    orig_clean = orig.strip()
    if orig_clean:
        found = False
        for trans in translated_paras:
            if len(trans.strip()) > 10:  # Pomiń bardzo krótkie
                found = True
                break
        if not found:
            missing.append(f"Brak {idx+1}: {orig_clean[:60]}")

if missing:
    print("\nUTRACONE ELEMENTY:")
    for m in missing:
        print(f"  ⚠ {m}")
