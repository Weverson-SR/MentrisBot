from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTextEdit, QLineEdit, QHBoxLayout, QFrame, QSizePolicy
from PyQt6.QtGui import QPalette, QColor, QIcon
from PyQt6.QtCore import Qt
from processo import ProcessoEmSegundoPlano
from mentris import Mentris

class MentrisApp(QWidget):
    def __init__(self):
        """
        Inicializa a aplicação Mentris.
        """
        super().__init__()

        self.init_ui()
        self.mentris = Mentris()

    def init_ui(self):
        """
        Configura a interface do usuário.
        """
        self.setWindowTitle("Mentris")
        self.setGeometry(100, 100, 800, 500)
        self.aplica_tema_escuro()

        self.interface = QVBoxLayout()
        self.interface.setContentsMargins(10, 10, 10, 10)  # Define margens externas

        # Caixa de Histórico de Chat
        self.tela_chat = QTextEdit()
        self.tela_chat.setReadOnly(True)
        self.tela_chat.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)  # Expande corretamente
        self.interface.addWidget(self.tela_chat)

        # Criando um QFrame para a Caixa de Entrada
        self.frame_mensagem = QFrame()

        # 📏 Layout da Caixa de Entrada + Botão
        hbox = QHBoxLayout(self.frame_mensagem)
        hbox.setContentsMargins(10, 5, 10, 5)

        self.caixa_mensagem = QLineEdit()
        self.caixa_mensagem.setPlaceholderText("Digite sua mensagem...")
        hbox.addWidget(self.caixa_mensagem)

        # Botão de Enviar
        self.botao_enviar = QPushButton()
        self.botao_enviar.setIcon(QIcon("flecha.png"))  # Ícone do botão
        self.botao_enviar.setIconSize(self.botao_enviar.sizeHint())  
        self.botao_enviar.setFixedSize(40, 40)  # Ajustando tamanho do botão
        self.botao_enviar.clicked.connect(self.enviar_mensagem)
        hbox.addWidget(self.botao_enviar)

        # Adiciona a caixa de entrada no final da interface
        self.interface.addWidget(self.frame_mensagem)

        self.setLayout(self.interface)
        self.aplica_estilo()

    def aplica_tema_escuro(self):
        """
        Aplica o tema escuro à interface.
        """
        paleta = QPalette()
        paleta.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
        paleta.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
        paleta.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
        self.setPalette(paleta)

    def aplica_estilo(self):
        """
        Aplica o estilo CSS à interface.
        """
        self.setStyleSheet("""
            QWidget {
                background-color: #353535;
                color: #ffffff;
                font-size: 14px;
            }
            QTextEdit {
                border: 1px solid #444444;
                border-radius: 10px;
                padding: 10px;
                background-color: #2b2b2b;
                color: #ffffff;
                font-size: 16px;
            }
            QFrame {
                border: 1px solid #444444;
                border-radius: 10px;
                background-color: #2b2b2b;
                padding: 5px;
            }
            QLineEdit {
                border: none;
                background-color: transparent;
                color: #ffffff;
                font-size: 16px;
            }
            QPushButton {
                border: none;
                border-radius: 20px;
                background-color: #2b2b2b;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #3c3c3c;
            }
            QPushButton:pressed {
                background-color: #1f1f1f;
            }
        """)

    def enviar_mensagem(self):
        """
        Envia a mensagem do usuário e inicia o processo de interação com o Mentris.
        """
        texto_usuario = self.caixa_mensagem.text().strip()
        if texto_usuario:
            self.tela_chat.append(f'🌌 Você: {texto_usuario}\n')
            self.processo = ProcessoEmSegundoPlano(self.mentris, texto_usuario)
            self.processo.termina.connect(self.mostrar_resposta)
            self.processo.start()
            self.caixa_mensagem.clear()

    def mostrar_resposta(self, resposta):
        """
        Mostra a resposta do Mentris na tela de chat.

        Args:
            resposta (str): Resposta gerada pelo Mentris.
        """
        self.tela_chat.append(f'🤖 Mentris: {resposta}\n')