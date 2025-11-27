"""
Test mechanizmu fallback tłumaczenia (Argos → NLLB)
"""
import sys

print("="*70)
print("TEST MECHANIZMU FALLBACK TŁUMACZENIA")
print("="*70)

# Test 1: Sprawdź Argos
print("\n[1/3] Sprawdzanie Argos Translate...")
argos_available = False
has_ru = False
has_uk = False

try:
    import argostranslate.translate
    
    installed = argostranslate.translate.get_installed_languages()
    print(f"✓ Argos zainstalowany, języków: {len(installed)}")
    
    if len(installed) == 0:
        print("  ⚠ Brak pakietów językowych")
    else:
        # Sprawdź pary językowe
        for src in installed:
            for tgt in installed:
                if src.code == "pl" and tgt.code == "en":
                    print(f"  ✓ PL → EN dostępne")
                if src.code == "pl" and tgt.code == "ru":
                    has_ru = True
                    print(f"  ✓ PL → RU dostępne")
                if src.code == "pl" and tgt.code == "uk":
                    has_uk = True
                    print(f"  ✓ PL → UK dostępne")
    
    argos_available = True
    
except Exception as e:
    print(f"  ✗ Argos niedostępny: {e}")

# Test 2: Sprawdź NLLB Fallback
print("\n[2/3] Sprawdzanie NLLB Fallback...")
nllb_available = False

try:
    from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
    import torch
    
    print("  ✓ Transformers dostępne")
    print("  ℹ NLLB może być użyty jako fallback dla RU/UK")
    nllb_available = True
    
except Exception as e:
    print(f"  ✗ NLLB niedostępny: {e}")

# Test 3: Symulacja logiki wyboru translatora
print("\n[3/3] Symulacja logiki wyboru translatora...")

def test_language(lang_code, lang_name):
    print(f"\n  Test: PL → {lang_name} ({lang_code})")
    
    if argos_available:
        # Sprawdź czy jest para w Argos
        if (lang_code == "ru" and has_ru) or (lang_code == "uk" and has_uk) or lang_code == "en":
            print(f"    ✓ Użyje: ARGOS (preferowane)")
            return "argos"
        else:
            print(f"    ⚠ Argos: brak pary językowej pl→{lang_code}")
    
    # Fallback dla RU/UK
    if lang_code in {"ru", "uk"} and nllb_available:
        print(f"    ✓ Użyje: NLLB FALLBACK (facebook/nllb-200-distilled-600M)")
        return "nllb"
    
    print(f"    ✗ Brak dostępnego tłumaczenia!")
    return None

# Testuj wszystkie języki
test_language("en", "Angielski")
test_language("ru", "Rosyjski")
test_language("uk", "Ukraiński")

# Podsumowanie
print("\n" + "="*70)
print("PODSUMOWANIE")
print("="*70)

print("\nMechanizm fallback:")
print("  1. Argos Translate (preferowane, szybkie, offline)")
print("  2. NLLB Model (fallback dla RU/UK, wolniejsze, offline)")
print("  3. Brak tłumaczenia (jeśli żaden nie działa)")

if not has_ru and not has_uk and nllb_available:
    print("\n⚠ REKOMENDACJA:")
    print("  Brak Argos dla RU/UK → użyje NLLB fallback")
    print("  Aby zainstalować Argos:")
    print("    python install_languages.py")

if argos_available and has_ru and has_uk:
    print("\n✓ Wszystkie tłumaczenia dostępne przez Argos (najszybsze)")

if not argos_available and not nllb_available:
    print("\n✗ BRAK TŁUMACZEŃ!")
    print("  Zainstaluj pakiety językowe: python install_languages.py")

print("="*70)
