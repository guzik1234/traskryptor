"""Test naprawy tłumaczenia kropek"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from pdf_translator import PDFTranslator

print("TEST NAPRAWY KROPEK - PL->UK\n")

translator = PDFTranslator(source_lang="pl", target_lang="uk")

# Test cases
test_cases = [
    "NIP..........................................................",
    "przedstawiony ..........................................",
    "Umowa Nr ..................",
    "§ 1",
    "§ 2",
    "Studenci Politechniki Białostockiej",
    "zawarta w dniu ........................... w ...........................",
]

print("Testowanie tłumaczenia z kropkami:\n")
for test in test_cases:
    result = translator._translate(test)
    print(f"IN:  {test[:60]}")
    print(f"OUT: {result[:60]}")
    print()

print("\n" + "="*60)
print("Test pełnego dokumentu...")
print("="*60)

success = translator.translate_docx_to_docx_and_pdf(
    input_path="Podanie o uznanie wykonanej pracy jako praktyki z nazwiskiem dziekana.odt",
    output_docx="TEST_DOTS_FIX_UK.docx",
    output_pdf="TEST_DOTS_FIX_UK.pdf"
)

if success:
    print("\n✅ KROPKI POPRAWIONE! Sprawdź pliki:")
    print("  - TEST_DOTS_FIX_UK.docx")
    print("  - TEST_DOTS_FIX_UK.pdf")
else:
    print("\n❌ BŁĄD")
