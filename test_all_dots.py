"""Test naprawy wszystkich kropek (3+)"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from pdf_translator import PDFTranslator

print("TEST NAPRAWY WSZYSTKICH KROPEK\n")

translator = PDFTranslator(source_lang="pl", target_lang="ru")

# Problematyczne przypadki
test_cases = [
    "zawarta w dniu ……………….. w ……………………pomiędzy:",
    "................................................... ... , w ........................................... ...",
    "NIP……………………………………………., KRS……………………………..",
    "daty od …. do",
    "§ 1",
    "Zakład pracy",
]

print("Testowanie z RU:\n")
for test in test_cases:
    result = translator._translate(test)
    print(f"IN:  '{test}'")
    print(f"OUT: '{result}'")
    print()

print("\n" + "="*70)
print("Jeśli widzisz oryginalne kropki (bez 'в период с') - DZIAŁA! ✅")
print("="*70)
