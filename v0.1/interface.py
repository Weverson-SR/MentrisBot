from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLineEdit, QPushButton, QApplication
)
from PyQt6.QtCore import QRunnable, QThreadPool, pyqtSlot, QObject, pyqtSignal
from PyQt6.QtGui import QColor, QPalette, QTextCursor
from mentris_01 import Mentris_01

# Sinais do Worker
class WorkerSignals(QObject):
    finished = pyqtSignal(str)  # sinal para enviar a resposta completa
    error = pyqtSignal(str)     # sinal para erros (opcional)

# Worker para processar o chat em segundo plano
class ChatWorker(QRunnable):
    def __init__(self, bot, user_input):
        super().__init__()
        self.bot = bot
        self.user_input = user_input
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            # Chama o método bloqueante que se comunica com o modelo
            resposta_completa = self.bot.processa_resposta(self.user_input)
        except Exception as e:
            self.signals.error.emit(str(e))
        else:
            self.signals.finished.emit(resposta_completa)

class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mentris Chat")
        self.setMinimumSize(600, 500)
        
        # Inicializar o bot (classe definida no mentris_01)
        self.bot = Mentris_01()
        
        # Configurar o widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        
        # Área de histórico do chat
        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        self.chat_history.setStyleSheet("""
            background-color: #2d2d2d;
            color: #ffffff;
            border: 1px solid #3d3d3d;
            border-radius: 5px;
            padding: 8px;
        """)
        main_layout.addWidget(self.chat_history)
        
        # Layout para entrada de texto e botão
        input_layout = QHBoxLayout()
        
        # Campo de entrada de texto
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Digite sua mensagem...")
        self.input_field.setStyleSheet("""
            background-color: #333333;
            color: #ffffff;
            border: 1px solid #3d3d3d;
            border-radius: 5px;
            padding: 8px;
        """)
        self.input_field.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.input_field)
        
        # Botão de enviar
        self.send_button = QPushButton("Enviar")
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #0d6efd;
                color: white;
                border-radius: 5px;
                padding: 8px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0b5ed7;
            }
            QPushButton:pressed {
                background-color: #0a58ca;
            }
        """)
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_button)
        
        main_layout.addLayout(input_layout)
        
        # Aplicando estilo geral da janela
        self.setStyleSheet("""
            QMainWindow {
                background-color: #212121;
            }
        """)
        
        # Limpar o histórico inicial e mostrar mensagem de boas-vindas
        self.chat_history.clear()
        self.append_message("Sistema", "Bem-vindo ao Mentris! Como posso ajudar?", "#8e8e8e")
        
        # Instância do QThreadPool para gerenciar os workers
        self.threadpool = QThreadPool()

    def append_message(self, sender, message, color):
        """Adiciona mensagem ao histórico do chat com formatação"""
        self.chat_history.setTextColor(QColor(color))
        self.chat_history.append(f"[{sender}]:")
        self.chat_history.setTextColor(QColor("#ffffff"))
        self.chat_history.append(f"{message}\n")
        
        # Rolar para a última mensagem
        cursor = self.chat_history.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.chat_history.setTextCursor(cursor)

    @pyqtSlot()
    def send_message(self):
        """Envia a mensagem do usuário e inicia o processamento em segundo plano"""
        user_input = self.input_field.text().strip()
        if not user_input:
            return
        
        # Adiciona a mensagem do usuário na interface
        self.append_message("Você", user_input, "#4da6ff")
        self.input_field.clear()
        
        # Indicar que está processando e desabilitar os controles
        self.append_message("Sistema", "Processando resposta...", "#8e8e8e")
        self.input_field.setEnabled(False)
        self.send_button.setEnabled(False)
        
        # Cria o worker que processa a resposta
        worker = ChatWorker(self.bot, user_input)
        worker.signals.finished.connect(self.handle_response)
        worker.signals.error.connect(self.handle_error)
        
        # Adiciona o worker à thread pool para execução
        self.threadpool.start(worker)

    @pyqtSlot(str)
    def handle_response(self, resposta_completa):
        """Atualiza a interface com a resposta do bot e atualiza o histórico de mensagens."""

        # Remove a mensagem de "Processando resposta..." 
        self.chat_history.undo()

        # (aqui, mostramos a resposta)
        self.append_message("Mentris", resposta_completa, "#00cc99")
        self.bot.atualiza_messages("", resposta_completa)

        # Reativa os controles da caixa de mensagem e do botão enviar
        self.input_field.setEnabled(True)
        self.send_button.setEnabled(True)
        self.input_field.setFocus()

    @pyqtSlot(str)
    def handle_error(self, error_message):
        """Trata erros na execução do worker."""
        self.append_message("Sistema", f"Erro: {error_message}", "#ff6666")
        self.input_field.setEnabled(True)
        self.send_button.setEnabled(True)
        self.input_field.setFocus()

def configurar_aparencia(app):
    """
    Configura a aparência escura para a aplicação.
    """
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(0, 0, 0))
    dark_palette.setColor(QPalette.ColorRole.ToolTipText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ColorRole.Text, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 0))
    dark_palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.ColorRole.HighlightedText, QColor(0, 0, 0))
    app.setPalette(dark_palette)

