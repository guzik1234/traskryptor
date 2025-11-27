"""Kopiuje zaktualizowane pliki z VFS repo do lokalnego katalogu"""
import shutil
import os

# Źródła (edytowane w repo VFS)
repo_base = r"vscode-vfs://github/guzik1234/traskryptor"

# Pliki do skopiowania
files_to_sync = [
    "translation_gui.py",
    "pdf_translator.py"
]

print("Synchronizacja plików z repo...")
for fname in files_to_sync:
    src = os.path.join(repo_base, fname)
    dst = fname
    try:
        # VFS paths need special handling - read from traskryptor/ subdir
        src_path = os.path.join(repo_base, "traskryptor", fname)
        print(f"  {fname}... (VFS path, needs manual copy)")
    except Exception as e:
        print(f"  ❌ {fname}: {e}")

print("\n⚠ UWAGA: Pliki w vscode-vfs wymagają ręcznego skopiowania.")
print("Zmiany zostały zapisane w repo. Aby zastosować lokalnie:")
print("1. Otwórz zmienione pliki w repo (vscode-vfs://github/...)")
print("2. Skopiuj zawartość")
print("3. Wklej do lokalnych plików")
print("\nLUB uruchom aplikację bezpośrednio - VS Code używa repo jako workspace.")
