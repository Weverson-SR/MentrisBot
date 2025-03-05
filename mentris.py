from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from pymongo import MongoClient


# Classe principal do chatbot Mentris
class Mentris:
    def __init__(self, model_name="mistral-nemo", mongo_uri="mongodb://localhost:27017/", db_name="mentris_db", collection_name="conversas", limite_historico=5):
        """
        Inicializa o chatbot Mentris com um modelo de linguagem, conexão ao MongoDB e limite de histórico.

        Args:
            model_name (str): Nome do modelo de linguagem a ser usado.
            mongo_uri (str): URI de conexão ao MongoDB.
            db_name (str): Nome do banco de dados no MongoDB.
            collection_name (str): Nome da coleção no MongoDB.
            history_limit (int): Limite de linhas de histórico a serem mantidas no banco de dados.
        """
        self.model = OllamaLLM(model=model_name)
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]
        self.limite_historico = limite_historico
        self.template = self.cria_template()
        self.chain = self.template | self.model

    def cria_template(self):
        """
        Cria o template de prompt para passar instruções ao chatbot Mentris.

        Returns:
            ChatPromptTemplate: Template de prompt configurado.
        """
        return ChatPromptTemplate.from_template(
            """
            Você é **Mentris**, um assistente virtual.  

            ### **Função**
            - Sua missão é **me ajudar a estudar e programar** especialmente em **Python** e outras linguagens.  

            ### ** Regras de Resposta**
            - **Idioma**: Sempre responda em **Português do Brasil**.    

            ### **Histórico**
            {contexto}

            ### **Pergunta do Usuário**
            {pergunta}
            """
        )

    def carregando_contexto(self):
        """
        Carrega o histórico de conversas do MongoDB.

        Returns:
            str: Conteúdo do histórico de conversas.
        """
        conversas = self.collection.find().sort("_id", -1).limit(self.limite_historico)
        contexto = ""
        for conversa in conversas:
            contexto = f"Você: {conversa['usuario_input']}\nMentris: {conversa['resposta_limpa']}\n" + contexto   
        return contexto

    def salva_contexto(self, usuario_input, resposta_limpa):
        """
        Salva a conversa no MongoDB.

        Args:
            usuario_input (str): Entrada do usuário.
            resposta_limpa (str): Resposta do Mentris.
        """
        self.collection.insert_one({"usuario_input": usuario_input, "resposta_limpa": resposta_limpa})

    def interagir(self, usuario_input):
        """
        Interage com o usuário, atualizando o contexto e gerando uma resposta.

        Args:
            usuario_input (str): Entrada do usuário.

        Returns:
            str: Resposta do Mentris.
        """
        # Carrega o contexto
        contexto = self.carregando_contexto()
        # Atualiza o contexto com a entrada do usuário
        contexto_atualizado = f"{contexto}Você: {usuario_input}\n"

        # Faz o invoke do Mentris para responder
        resposta = self.chain.invoke({"contexto": contexto_atualizado, "pergunta": usuario_input})
        # Limpa a resposta para evitar duplicações no nome dele e na pergunta
        resposta_limpa = resposta.replace("Mentris:", "").replace("Resposta:", "").strip()

        # Salva o contexto com a resposta gerada
        self.salva_contexto(usuario_input, resposta_limpa)
        return resposta_limpa