import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os


class TranslationGUI:
    """Interfejs graficzny dla tłumaczenia PDF"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tłumaczenie dokumentów PDF")
        self.root.geometry("650x650")
        self.root.resizable(False, False)
        
        self.input_file = None
        self.output_file = None
        self.is_translating = False
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Tworzy widgety interfejsu"""
        
        # Tytuł
        title = tk.Label(self.root, text="Tłumaczenie dokumentów PDF", 
                        font=("Arial", 16, "bold"))
        title.pack(pady=20)
        
        # Wybór pliku wejściowego
        file_frame = tk.Frame(self.root)
        file_frame.pack(pady=10, padx=30, fill='x')
        
        tk.Label(file_frame, text="Plik Word/ODT (.docx/.odt) do przetłumaczenia:", 
                font=("Arial", 11)).pack(anchor='w')
        
        input_frame = tk.Frame(file_frame)
        input_frame.pack(fill='x', pady=5)
        
        self.input_label = tk.Label(input_frame, text="Nie wybrano pliku", 
                                    font=("Arial", 10), fg="gray", anchor='w')
        self.input_label.pack(side='left', fill='x', expand=True)
        
        tk.Button(input_frame, text="Wybierz plik", command=self.select_input_file,
                 font=("Arial", 10), bg="#2196F3", fg="white").pack(side='right', padx=5)
        
        # Język docelowy
        lang_frame = tk.Frame(self.root)
        lang_frame.pack(pady=20, padx=30)
        
        tk.Label(lang_frame, text="Przetłumacz z polskiego na:", 
                font=("Arial", 12, "bold")).pack(anchor='w', pady=5)
        
        self.target_lang = tk.StringVar(value="en")
        
        tk.Radiobutton(lang_frame, text="Angielski", variable=self.target_lang, 
                  value="en", font=("Arial", 11)).pack(anchor='w', padx=20, pady=3)
        tk.Radiobutton(lang_frame, text="Rosyjski", variable=self.target_lang, 
                  value="ru", font=("Arial", 11)).pack(anchor='w', padx=20, pady=3)
        tk.Radiobutton(lang_frame, text="Ukraiński", variable=self.target_lang, 
                  value="uk", font=("Arial", 11)).pack(anchor='w', padx=20, pady=3)
        
        # Tryb tłumaczenia (tylko Word)
        self.translation_mode = tk.StringVar(value="word")
        
        # Pasek postępu
        self.progress_frame = tk.Frame(self.root)
        self.progress_frame.pack(pady=15, padx=30, fill='x')
        
        self.progress_label = tk.Label(self.progress_frame, text="", font=("Arial", 10))
        self.progress_label.pack()
        
        self.progress_bar = ttk.Progressbar(self.progress_frame, mode='determinate', length=400)
        self.progress_bar.pack(pady=5)
        
        # Dodatkowy mały przycisk obok wyboru pliku (redundancja)
        small_btn = tk.Button(input_frame, text="Tłumacz", command=self.start_translation,
                      font=("Arial", 10), bg="#4CAF50", fg="white")
        small_btn.pack(side='right', padx=5)

        # Przyciski (dokowane na dole okna)
        bottom_bar = tk.Frame(self.root)
        bottom_bar.pack(side='bottom', fill='x')

        self.translate_button = tk.Button(bottom_bar, text="🚀 Rozpocznij tłumaczenie", 
                          command=self.start_translation,
                          font=("Arial", 13, "bold"), bg="#4CAF50", 
                          fg="white", height=2,
                          cursor="hand2")
        self.translate_button.pack(pady=10)
        
        # Przycisk powrotu do menu
        self.back_button = tk.Button(bottom_bar, text=" Powrót do menu", 
                          command=self._on_back_clicked,
                          font=("Arial", 11), bg="#FF9800", 
                          fg="white", height=1)
        self.back_button.pack(pady=5)
        
        # Status
        self.status_label = tk.Label(self.root, text="Wybierz plik PDF do przetłumaczenia", 
                                     font=("Arial", 10), fg="gray")
        self.status_label.pack(pady=5)
    
    def select_input_file(self):
        """Otwiera dialog wyboru pliku"""
        filename = filedialog.askopenfilename(
            title="Wybierz plik Word lub ODT",
            filetypes=[("Dokumenty Word/ODT", "*.docx *.odt"), ("Pliki Word", "*.docx"), ("Pliki ODT", "*.odt"), ("Wszystkie pliki", "*.*")]
        )
        
        if filename:
            self.input_file = filename
            self.input_label.config(text=os.path.basename(filename), fg="black")
            
            # Przygotuj nazwy plików wyjściowych (PDF i DOCX)
            base_name = os.path.splitext(filename)[0]
            # Dobierz sufiks na podstawie języka docelowego
            lang_map = {"en": "_en", "ru": "_ru", "uk": "_uk"}
            lang_suffix = lang_map.get(self.target_lang.get(), "_en")
            self.output_file_pdf = f"{base_name}{lang_suffix}.pdf"
            self.output_file_docx = f"{base_name}{lang_suffix}.docx"
            
            self.status_label.config(text="Plik wybrany. Gotowy do tłumaczenia.", fg="green")
    
    def start_translation(self):
        """Rozpoczyna proces tłumaczenia"""
        if not self.input_file:
            messagebox.showerror("Błąd", "Wybierz plik PDF do przetłumaczenia!")
            return
        
        if self.is_translating:
            return
        
        self.is_translating = True
        self.translate_button.config(state="disabled")
        self.status_label.config(text="Tłumaczenie w toku...", fg="orange")
        
        # Uruchom tłumaczenie w osobnym wątku
        thread = threading.Thread(target=self._translate_worker, daemon=True)
        thread.start()
    
    def _translate_worker(self):
        """Worker wykonujący tłumaczenie w tle"""
        from pdf_translator import PDFTranslator
        
        try:
            # Utwórz translator
            translator = PDFTranslator(
                source_lang="pl",
                target_lang=self.target_lang.get()
            )
            
            # Callback do aktualizacji postępu (PDF ścieżka)
            def update_progress(current, total):
                progress = (current / total) * 100
                self.root.after(0, lambda: self.progress_bar.config(mode='determinate', value=progress))
                self.root.after(0, lambda: self.progress_label.config(
                    text=f"Strona {current} z {total}"
                ))

            mode = self.translation_mode.get()
            if mode == "word":
                # Tryb Word – tłumacz DOCX → DOCX + PDF
                self.root.after(0, lambda: self.progress_bar.config(mode='indeterminate'))
                self.root.after(0, lambda: self.progress_bar.start(50))
                self.root.after(0, lambda: self.progress_label.config(text="Tłumaczenie Word (zapisz DOCX i PDF)..."))
                success = translator.translate_docx_to_docx_and_pdf(
                    self.input_file,
                    self.output_file_docx,
                    self.output_file_pdf
                )
            else:
                # Fallback (nie powinno wystąpić, ale dla bezpieczeństwa)
                success = False
            
            if success:
                self.root.after(0, lambda: self.status_label.config(
                    text=f"Tłumaczenie zakończone! DOCX: {os.path.basename(self.output_file_docx)}, PDF: {os.path.basename(self.output_file_pdf)}", 
                    fg="green"
                ))
                self.root.after(0, lambda: messagebox.showinfo(
                    "Sukces", 
                    f"Dokument został przetłumaczony!\n\nZapisano jako:\nWord: {self.output_file_docx}\nPDF: {self.output_file_pdf}"
                ))
            else:
                self.root.after(0, lambda: self.status_label.config(
                    text="Błąd podczas tłumaczenia", fg="red"
                ))
                self.root.after(0, lambda: messagebox.showerror(
                    "Błąd", 
                    "Wystąpił błąd podczas tłumaczenia dokumentu."
                ))
        
        except Exception as e:
            self.root.after(0, lambda: self.status_label.config(
                text=f"Błąd: {str(e)}", fg="red"
            ))
            self.root.after(0, lambda: messagebox.showerror("Błąd", str(e)))
        
        finally:
            self.root.after(0, lambda: self.translate_button.config(state="normal"))
            self.root.after(0, lambda: self.progress_bar.stop())
            self.root.after(0, lambda: self.progress_bar.config(mode='determinate', value=0))
            self.root.after(0, lambda: self.progress_label.config(text=""))
            self.is_translating = False
    
    def _on_back_clicked(self):
        """Obsługa kliknięcia przycisku Powrót"""
        self.root.destroy()
        from main import MainApp
        app = MainApp()
        app.run()
    
    def run(self):
        """Uruchamia GUI"""
        self.root.mainloop()


