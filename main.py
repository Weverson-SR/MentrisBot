import sys
from PyQt6.QtWidgets import QApplication
from interface import MentrisApp

# Função principal para iniciar a aplicação
if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = MentrisApp()
    janela.show()
    sys.exit(app.exec())