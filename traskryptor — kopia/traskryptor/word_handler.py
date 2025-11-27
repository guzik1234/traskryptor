import win32com.client


class WordHandler:
    """Obsługuje integrację z Microsoft Word"""
    
    def __init__(self):
        self.word = None
        self.doc = None
    
    def connect(self):
        """Łączy się z otwartą instancją Word"""
        try:
            self.word = win32com.client.GetActiveObject("Word.Application")
            self.doc = self.word.ActiveDocument
            return True
        except:
            return False
    
    def insert_text(self, text):
        """Wstawia tekst do dokumentu Word"""
        if self.word:
            self.word.Selection.InsertAfter(text + " ")
            self.word.Selection.MoveRight()
