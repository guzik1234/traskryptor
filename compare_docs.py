"""Porównuje dwa dokumenty (ODT/DOCX) paragraf po paragrafie.
Użycie: python compare_docs.py <oryginał.odt/docx> <przetłumaczony.docx>
"""
import sys
import os
import re
import win32com.client as win32

def main():
    if len(sys.argv) < 3:
        print("Użycie: python compare_docs.py <oryginał.odt/docx> <przetłumaczony.docx>")
        return

    src_path = os.path.abspath(sys.argv[1])
    dst_path = os.path.abspath(sys.argv[2])

    print("Sprawdzanie oryginalnego dokumentu...")
    word = win32.Dispatch("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0

    # Oryginalny
    doc1 = word.Documents.Open(src_path, ReadOnly=True)
    print(f"ORYGINALNY - Paragrafy: {doc1.Paragraphs.Count}")

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
    doc2 = word.Documents.Open(dst_path, ReadOnly=True)
    print(f"PRZETŁUMACZONY - Paragrafy: {doc2.Paragraphs.Count}")

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

    # Analiza linii z kropkami (formularzowe linie)
    def is_dots_line(s: str) -> bool:
        t = s.strip()
        core = re.sub(r"[\s\.·•–—\-…_]+", "", t)
        return len(core) == 0

    dots_original = sum(1 for p in original_paras if is_dots_line(p))
    dots_translated = sum(1 for p in translated_paras if is_dots_line(p))
    print(f"Linie formularzowe z kropkami: oryginal={dots_original}, tłumaczony={dots_translated}")

    # Pokaż przykładowe takie linie
    print("\nPrzykładowe linie z kropkami (oryginał → tłumaczenie):")
    count = 0
    for i in range(min(len(original_paras), len(translated_paras))):
        if is_dots_line(original_paras[i]) or is_dots_line(translated_paras[i]):
            print(f"  {i+1}: '{original_paras[i][:40]}' → '{translated_paras[i][:40]}'")
            count += 1
            if count >= 10:
                break

if __name__ == "__main__":
    main()
