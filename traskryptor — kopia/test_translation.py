"""Test tłumaczenia - sprawdza czy pakiety językowe działają"""
import argostranslate.package
import argostranslate.translate

print("=== TEST TŁUMACZENIA ===\n")

# Sprawdź zainstalowane języki
print("1. Sprawdzam zainstalowane języki...")
installed = argostranslate.translate.get_installed_languages()
print(f"   Znaleziono {len(installed)} języków:")
for lang in installed:
    print(f"   - {lang.name} ({lang.code})")

if len(installed) == 0:
    print("\n2. Brak języków! Instaluję pakiety...")
    argostranslate.package.update_package_index()
    available = argostranslate.package.get_available_packages()
    
    # Zainstaluj polski -> angielski
    for pkg in available:
        if pkg.from_code == "pl" and pkg.to_code == "en":
            print(f"   Pobieranie {pkg.from_name} -> {pkg.to_name}...")
            argostranslate.package.install_from_path(pkg.download())
            print("   Zainstalowano!")
            break
    
    # Odśwież listę
    installed = argostranslate.translate.get_installed_languages()

# Znajdź polsko-angielskie tłumaczenie
print("\n3. Szukam translatora polski -> angielski...")
pl = None
en = None

for lang in installed:
    if lang.code == "pl":
        pl = lang
    if lang.code == "en":
        en = lang

if pl and en:
    translator = pl.get_translation(en)
    print(f"   Znaleziono: {pl.name} -> {en.name}")
    
    # Test tłumaczenia
    print("\n4. Test tłumaczenia...")
    test_text = "Witaj świecie! To jest test tłumaczenia."
    print(f"   Oryginalny tekst: {test_text}")
    
    translated = translator.translate(test_text)
    print(f"   Przetłumaczone: {translated}")
    
    if translated and translated != test_text:
        print("\n✅ SUKCES! Tłumaczenie działa!")
    else:
        print("\n❌ BŁĄD! Tłumaczenie nie działa poprawnie.")
else:
    print("\n❌ BŁĄD! Nie znaleziono pakietów językowych.")
    print("   Uruchom: python install_languages.py")
