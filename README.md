# Mentris

Mentris é um chatbot de inteligência artificial desenvolvido para rodar localmente, combinando o modelo Mistral com o Ollama e armazenando o histórico de conversas no MongoDB. Ele possui uma interface gráfica criada com PyQt6 e é totalmente personalizável, permitindo adaptações de nome, modelo e comportamento.

## Diferenciais

- **Execução local**: Sem dependência de servidores externos, garantindo privacidade.
- **Histórico de conversas**: Armazena interações no MongoDB para respostas mais contextuais.
- **Interface moderna**: Desenvolvida em PyQt6, com tema escuro para conforto visual.
- **Flexibilidade de modelos**: Usa o Ollama para gerenciar modelos, permitindo substituição fácil.
- **Personalização do nome e estilo**: O bot pode ser renomeado e configurado conforme preferência.
- **Desempenho**: Para respostas mais rápidas,o sistema pode exigir um certo nivel de poder de processamento da sua maquina dependendo do modelo e volume de interações.

## Funcionalidades

- **Respostas objetivas e contextuais** com base no histórico de interações.
- **Interface intuitiva** para uma experiência fluida.
- **Modo de execução otimizado** com uso de threads para maior desempenho.
- **Armazenamento estruturado** no MongoDB para recuperação de contexto.
- **Fácil personalização** do modelo de IA, interface e comportamento.

## Estrutura do Projeto

- `main.py` - Arquivo principal que inicia a aplicação.
- `interface.py` - Define a interface gráfica com PyQt6.
- `mentris.py` - Implementa a lógica do chatbot, interação com o modelo e MongoDB.
- `processo.py` - Gerencia interações assíncronas usando QThread.
- `flecha.png` - Ícone da interface.
- `.gitignore` - Lista arquivos e pastas a serem ignorados no repositório.

## Como Executar

1. Instale as dependências necessárias:

```sh
pip install -r requirements.txt
```

2. Instale o Ollama, se ainda não tiver:

```sh
curl -fsSL https://ollama.com/install.sh | sh
```

3. Escolha e baixe um modelo de IA pelo Ollama, por exemplo, o Mistral:

```sh
ollama pull mistral-nemo
```

4. Execute o arquivo principal:

```sh
python main.py
```

## Dependências

- PyQt6
- langchain\_ollama
- langchain\_core
- pymongo

## Configuração do Ollama

O Mentris usa o Ollama para gerenciar modelos de IA. Para trocar o modelo, edite o parâmetro `model_name` na classe `Mentris` no arquivo [`mentris.py`](mentris.py):

```python
self.model_name = "mistral-nemo"
```

Caso queira usar outro modelo, basta alterá-lo para qualquer modelo disponível no Ollama.

## Personalização do Nome

O nome "Mentris" é apenas um exemplo. Você pode personalizar o chatbot conforme desejar, modificando a interface e os textos no código-fonte.

## Inspiração e Desenvolvimento

Este projeto foi criado como parte dos meus estudos em Python e IA, sendo uma evolução de um chatbot anterior baseado no modelo Gemini [acesse aqui](https://github.com/Weverson-SR/Projeto_ChatBot).

### Melhorias Futuras

1. **Aprendizado Contínuo com IA**: Pretendo implementar uma IA que possa aprender de forma contínua, permitindo ao Mentris adaptar suas respostas e comportamento com base nas interações anteriores, proporcionando uma experiência cada vez mais personalizada e natural.

2. **Processamento de Respostas com IA Intermediária**: A futura implementação de uma IA intermediária irá otimizar o fluxo de processamento das respostas, permitindo uma análise preliminar das interações antes que a resposta final seja gerada, o que resultará em um desempenho mais ágil e preciso.

3. **Sistema de Feedback e Memória Persistente**: Planejo integrar um sistema de feedback que, junto com a memória persistente, permitirá que o Mentris aprenda com o usuário ao longo do tempo, ajustando seu comportamento e respostas de forma contínua. Isso proporcionará uma interação mais fluida e adaptativa.

4. **Detecção de Emoções**: Em uma atualização futura, o Mentris será capaz de detectar emoções na escrita ou fala usuário, como "raiva" ou "felicidade", e ajustar suas respostas de acordo, criando uma experiência mais empática e humanizada.

## ✨ Contribuição

Se quiser sugerir melhorias, relatar bugs ou contribuir com código, fique à vontade para enviar pull requests!

## ⚖️ Licença

Este projeto está licenciado sob a Licença MIT.
