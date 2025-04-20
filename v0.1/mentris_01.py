from ollama import chat

class Mentris_01:
    def __init__(self):
        # Inicializa o histórico de mensagens
        self.messages = [
            {'role': 'user', 'content': 'content'},
            {'role': 'assistant', 'content': 'content'}
        ]

    def processa_resposta(self, user_input):
        """Processa a resposta do modelo e retorna a resposta completa."""
        response_stream = chat(
            model='gemma3:1b',
            messages=self.messages + [{'role': 'user', 'content': user_input}],
            stream=True,
        )

        resposta_completa = ""
        for chunk in response_stream:
            content = chunk['message']['content']
            # print(content, end='', flush=True)  # Imprime a resposta em tempo real
            resposta_completa += content  # Concatena os pedaços da resposta

        # print('\n')  # Quebra de linha após a resposta completa
        return resposta_completa

    def atualiza_messages(self, user_input, resposta_assistente):
        """Atualiza o histórico de mensagens."""
        self.messages += [
            {'role': 'user', 'content': user_input},
            {'role': 'assistant', 'content': resposta_assistente}
        ]
