from PyQt6.QtCore import QThread, pyqtSignal

class ProcessoEmSegundoPlano(QThread):
    termina = pyqtSignal(str)

    def __init__(self, mentris, texto_usuario):
        """
        Inicializa o processo em segundo plano.

        Args:
            mentris (Mentris): Instância do chatbot Mentris.
            texto_usuario (str): Entrada do usuário.
        """
        super().__init__()
        self.mentris = mentris
        self.texto_usuario = texto_usuario

    def run(self):
        """
        Executa a interação com o Mentris em segundo plano e emite o sinal com a resposta.
        """
        resposta = self.mentris.interagir(self.texto_usuario)
        self.termina.emit(resposta)