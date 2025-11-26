"""Test tłumaczenia małego fragmentu dokumentu"""
import os
import sys

# Test z pierwszymi 3 akapitami
odt_path = r"c:\Transkrybcja\traskryptor\Podanie o uznanie wykonanej pracy jako praktyki z nazwiskiem dziekana.odt"
output_docx = r"c:\Transkrybcja\traskryptor\TEST_MINI_EN.docx"
output_pdf = r"c:\Transkrybcja\traskryptor\TEST_MINI_EN.pdf"

print("Mini test tłumaczenia (tylko 3 pierwsze akapity)")
print("="*60)

try:
    from pdf_translator import PDFTranslator
    from deep_translator import GoogleTranslator
    
    # Test translacji
    print("\n1. Test API tłumaczenia:")
    translator = GoogleTranslator(source='pl', target='en')
    test_text = "Białystok, 2024"
    result = translator.translate(test_text)
    print(f"   '{test_text}' → '{result}'")
    if not result:
        print("✗ BŁĄD: Translator nie działa!")
        sys.exit(1)
    print("   ✓ Translator działa")
    
except Exception as e:
    print(f"✗ BŁĄD importu: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n2. Test tłumaczenia dokumentu:")
print("   (Tylko pierwsze 3 akapity dla szybkości)")

try:
    import win32com.client as win32
    
    word = win32.Dispatch("Word.Application")
    word.Visible = True  # WIDOCZNY aby obserwować proces
    word.DisplayAlerts = 0
    print("   ✓ Word uruchomiony")
    
    doc = word.Documents.Open(odt_path, ReadOnly=False, ConfirmConversions=False)
    print(f"   ✓ Dokument otwarty ({doc.Paragraphs.Count} akapitów)")
    
    # Pobierz stałe Word po uruchomieniu
    import win32com.client
    wd = win32com.client.constants
    translator = GoogleTranslator(source='pl', target='en')
    
    # Tłumacz tylko pierwsze 3 akapity
    count = 0
    for i in range(1, min(4, doc.Paragraphs.Count + 1)):
        p = doc.Paragraphs.Item(i)
        original = p.Range.Text.rstrip("\r")
        
        # Pomiń puste
        if not original.strip():
            continue
            
        print(f"\n   Akapit {i}:")
        print(f"     PL: '{original[:60]}'")
        
        try:
            translated = translator.translate(original)
            p.Range.Text = translated + "\r"
            print(f"     EN: '{translated[:60]}'")
            count += 1
        except Exception as e:
            print(f"     ⚠ Błąd tłumaczenia: {e}")
    
    print(f"\n   ✓ Przetłumaczono {count} akapitów")
    
    # Zapisz
    print(f"\n3. Zapisywanie:")
    abs_docx = os.path.abspath(output_docx)
    abs_pdf = os.path.abspath(output_pdf)
    
    print(f"   DOCX: {os.path.basename(abs_docx)}")
    # FileFormat: 12 = wdFormatXMLDocument (DOCX)
    doc.SaveAs2(abs_docx, FileFormat=12)
    print("   ✓ DOCX zapisany")
    
    print(f"   PDF: {os.path.basename(abs_pdf)}")
    # ExportFormat: 17 = wdExportFormatPDF
    doc.ExportAsFixedFormat(OutputFileName=abs_pdf, ExportFormat=17)
    print("   ✓ PDF zapisany")
    
    doc.Close(SaveChanges=False)
    word.Quit()
    print("\n   ✓ Word zamknięty")
    
    print("\n" + "="*60)
    print("✓✓✓ TEST ZAKOŃCZONY SUKCESEM ✓✓✓")
    print("="*60)
    
except Exception as e:
    print(f"\n✗ BŁĄD: {e}")
    import traceback
    traceback.print_exc()
    try:
        if 'doc' in locals():
            doc.Close(SaveChanges=False)
        if 'word' in locals():
            word.Quit()
    except:
        pass
