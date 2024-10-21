from langchain_openai import ChatOpenAI  # Importa o módulo ChatOpenAI da biblioteca LangChain, para conectar-se ao modelo GPT da OpenAI
from langchain_core.prompts import ChatPromptTemplate  # Importa o template de prompts para a interação com a LLM
from langchain_core.output_parsers import StrOutputParser  # Importa o parser para processar a saída em formato de string
from langchain_core.runnables import RunnableParallel, RunnablePassthrough  # Importa módulos que permitem a execução paralela e a passagem direta de dados
from dotenv import load_dotenv  # Importa o dotenv para carregar variáveis de ambiente do arquivo .env
from langchain.memory import ConversationBufferMemory
import os  # Módulo para interagir com o sistema operacional

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configura a chave da API da OpenAI no ambiente, que será usada para autenticar as chamadas à API
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

## Configuração do Template

# Instancia o modelo GPT-4 da OpenAI com um nível de temperatura 0.0, o que significa que o modelo será determinístico
llm = ChatOpenAI(model_name="gpt-4o", temperature=0.0)

# Template de prompt que será passado ao modelo para gerar lições diárias
template = """
Você é um especialista em educação e foi encarregado de gerar lições diárias curtas, entre 10 e 15 minutos de leitura, com base em uma ementa de estudo. A ementa já foi aprovada, e agora sua função é criar lições com conteúdos coesos e organizados. Cada lição deve ter um foco claro, progressivo e ser fácil de entender.

Sua função agora é gerar a lição baseada no tópico abaixo, dividindo-a em subtópicos quando necessário. Sempre que possível, inclua exemplos práticos ou análises curtas de obras/textos relevantes. A lição também deve ter um exercício ou questão reflexiva no final para fixar o aprendizado.

Aqui está o contexto e as regras que você deve seguir ao criar a lição:

1. **Tópico do Dia**: {input}.
2. **Objetivo**: Apresentar o conteúdo de maneira simples e progressiva, garantindo que o aluno entenda o conceito de forma clara e prática.
3. **Estrutura**:
   - Introduza o conceito de forma clara e objetiva.
   - Detalhe os pontos principais, incluindo exemplos práticos quando aplicável.
   - Se houver alguma obra ou texto relevante, inclua uma análise ou resumo do trecho.
   - Finalize com uma pergunta reflexiva ou sugestão de exercício prático.
4. **Tamanho**: Mantenha o conteúdo adequado para ser lido em 10 a 15 minutos.

Agora, com base nessas instruções, crie uma lição de qualidade.
"""

# Constrói o template de prompt a partir da string anterior
template_prompt = ChatPromptTemplate.from_template(template)

# Define um parser para transformar a saída do modelo em uma string
output_parser = StrOutputParser()

## Configuração da Pipeline

# Configura um "retriever" que passará o input diretamente para o próximo componente do pipeline
setup_retrievel = RunnableParallel(
    {
        "input": RunnablePassthrough() # O RunnablePassthrough permite a passagem do input sem modificações
    }
)

# Cria a pipeline, que executa em sequência:
# 1. O input (tópico do dia) é passado diretamente.
# 2. O template do prompt é aplicado, gerando o texto a ser enviado ao modelo.
# 3. O modelo da OpenAI (GPT-4) é chamado para gerar a resposta.
# 4. A saída é processada pelo output_parser, que transforma o resultado final em string.
chain = setup_retrievel | template_prompt | llm | output_parser

# Invoca a pipeline com o input fornecido (tópico da lição) e obtém a resposta gerada
response = chain.invoke("Introdução aos conceitos básicos da psicologia analítica e seus objetivos")

# Formata a resposta, adicionando uma linha em branco após cada nova linha para melhorar a legibilidade
formatted_response = response.replace("\n", "\n\n")

# Imprime a resposta formatada
print(formatted_response)
