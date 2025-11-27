# Rozwiązanie problemu z tłumaczeniem dokumentów

## Problem
Program zgłaszał błąd podczas tłumaczenia dokumentów Word/ODT. Proces się zawieszał bez komunikatu błędu.

## Przyczyna
Biblioteka `win32com.client.constants` nie była dostępna w trybie niewidocznym Microsoft Word, co powodowało:
- Zawieszanie się procesu Word podczas uruchamiania
- Brak dostępu do stałych Word (wdFormatXMLDocument, wdExportFormatPDF itp.)
- Nieobsłużone wyjątki przy próbie użycia stałych

## Rozwiązanie
1. **Usunięto import `win32com.client.constants`** 
2. **Zastąpiono wszystkie stałe Word wartościami numerycznymi:**
   - `wdMainTextStory` → `1`
   - `wdTextFrameStory` → `3`
   - `wdFormatXMLDocument` → `12` (DOCX)
   - `wdExportFormatPDF` → `17` (PDF)
   - `wdFormatPDF` → `17` (PDF SaveAs2)
   - `wdPrimaryHeaderStory` → `5`
   - `wdPrimaryFooterStory` → `6`

3. **Dodano szczegółowe logowanie:**
   - Postęp tłumaczenia w 7 krokach
   - Liczniki przetłumaczonych akapitów
   - Informacje o błędach z traceback
   - Status zapisu plików

## Zmiany w kodzie

### pdf_translator.py
```python
# PRZED:
from win32com.client import constants as wd
doc.SaveAs2(output_docx, FileFormat=wd.wdFormatXMLDocument)

# PO:
# FileFormat: 12 = wdFormatXMLDocument (DOCX)
doc.SaveAs2(output_docx, FileFormat=12)
```

## Wynik
✓ Tłumaczenie dokumentu ODT (46 akapitów) działa poprawnie
✓ Pliki DOCX i PDF są tworzone i zapisywane
✓ Szczegółowe logowanie pozwala śledzić postęp
✓ Obsługa błędów zapewnia czytelne komunikaty

## Test
Przetestowano na pliku:
- **Wejście:** `Podanie o uznanie wykonanej pracy jako praktyki z nazwiskiem dziekana.odt`
- **Wyjście:** `Podanie_FINAL_EN.docx` (15.9 KB) + `Podanie_FINAL_EN.pdf` (104 KB)
- **Czas:** ~1.5 minuty dla 46 akapitów (13 przetłumaczonych fragmentów)
- **Status:** ✓✓✓ SUKCES ✓✓✓

## Jak używać

### Przez GUI:
```bash
python main.py
```
1. Wybierz "Tłumaczenie dokumentów"
2. Kliknij "Wybierz plik" i wskaż dokument .docx lub .odt
3. Wybierz język docelowy (English / Русский)
4. Poczekaj na zakończenie tłumaczenia

### Z linii poleceń:
```python
from pdf_translator import PDFTranslator

translator = PDFTranslator('pl', 'en')
translator.translate_docx_to_docx_and_pdf(
    input_path='dokument.odt',
    output_docx='dokument_en.docx',
    output_pdf='dokument_en.pdf'
)
```

## Uwagi techniczne
- Wymaga zainstalowanego Microsoft Word (testowane na Office 2013/Office 15)
- Word jest uruchamiany w trybie niewidocznym (Visible=False)
- Funkcja pomija puste akapity i pojedyncze znaki interpunkcyjne
- Tłumaczenie używa Google Translate API (wymaga połączenia z internetem)
- Zachowana jest pełna struktura dokumentu (formatowanie, układ, czcionki)

## Diagnostyka
Jeśli wystąpią problemy, uruchom test:
```bash
python test_mini_translate.py  # Test z pierwszymi 3 akapitami
python test_word_visible.py    # Test z widocznym Word (aby zobaczyć dialogi)
```
