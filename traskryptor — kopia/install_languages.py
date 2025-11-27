"""
Skrypt do instalacji pakietów językowych dla Argos Translate
Uruchom ten skrypt raz, aby zainstalować pakiety offline
"""

import argostranslate.package
import argostranslate.translate


def install_language_packages():
    """Instaluje pakiety językowe dla tłumaczenia offline"""
    
    print("Aktualizacja indeksu pakietów...")
    argostranslate.package.update_package_index()
    
    print("Pobieranie listy dostępnych pakietów...")
    available_packages = argostranslate.package.get_available_packages()
    
    # Pakiety do zainstalowania
    to_install = [
        ("pl", "en"),  # Polski -> Angielski
        ("pl", "ru"),  # Polski -> Rosyjski
    ]
    
    for source, target in to_install:
        print(f"\nSzukanie pakietu {source} -> {target}...")
        
        package = None
        for pkg in available_packages:
            if pkg.from_code == source and pkg.to_code == target:
                package = pkg
                break
        
        if package:
            print(f"Pobieranie i instalacja pakietu {package.from_name} -> {package.to_name}...")
            try:
                download_path = package.download()
                argostranslate.package.install_from_path(download_path)
                print(f"✓ Zainstalowano: {package.from_name} -> {package.to_name}")
            except Exception as e:
                print(f"✗ Błąd instalacji: {e}")
        else:
            print(f"✗ Nie znaleziono pakietu {source} -> {target}")
    
    print("\n" + "="*50)
    print("Zainstalowane pakiety językowe:")
    installed = argostranslate.translate.get_installed_languages()
    for lang in installed:
        print(f"  - {lang.name} ({lang.code})")
    
    print("\n✓ Instalacja zakończona!")
    print("Tłumaczenie PDF będzie teraz działać w pełni OFFLINE.")


if __name__ == "__main__":
    install_language_packages()
