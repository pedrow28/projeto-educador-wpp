import pandas as pd
from langchain_openai import ChatOpenAI  # Importa o módulo ChatOpenAI da biblioteca LangChain, para conectar-se ao modelo GPT da OpenAI
from langchain_core.prompts import ChatPromptTemplate  # Importa o template de prompts para a interação com a LLM
from langchain_core.output_parsers import StrOutputParser  # Importa o parser para processar a saída em formato de string
from langchain_core.runnables import RunnableParallel, RunnablePassthrough  # Importa módulos que permitem a execução paralela e a passagem direta de dados
from dotenv import load_dotenv  # Importa o dotenv para carregar variáveis de ambiente do arquivo .env
import os  # Módulo para interagir com o sistema operacional
from twilio.rest import Client  # Importa o módulo Twilio para enviar mensagens via WhatsApp
import pywhatkit as kit # Importa o módulo pywhatkit para enviar SMS via WhatsApp

## Configurações

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Credenciais do Twilio
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
twilio_whatsapp_number = os.getenv('TWILIO_WHATSAPP_NUMBER')

# Configura a chave da API da OpenAI no ambiente, que será usada para autenticar as chamadas à API
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Instancia o modelo GPT-4 da OpenAI com um nível de temperatura 0.0, o que significa que o modelo será determinístico
llm = ChatOpenAI(model_name="gpt-4o", temperature=0.0)

## Funções

# Extrair ementa
def extrair_ementa(path_excel, path_txt):

    """
    Esta função extrai a lição diária com base no dia atual a partir de um arquivo Excel e um arquivo de texto.

    Args:
        path_excel (str): O caminho para o arquivo Excel que contém as lições.
        path_txt (str): O caminho para o arquivo de texto com a informação do dia atual.

    Returns:
        numpy.ndarray: Um array contendo a descrição da lição para o dia atual.
    """

    # Abre o arquivo Excel

    arquivo_excel = path_excel  # Substitua pelo caminho do seu arquivo
    planilha = pd.read_excel(arquivo_excel) 

    # Cria uma lista vazia para armazenar os texto
    # Abrir e ler o arquivo txt
    with open(path_txt, 'r') as arquivo:
        conteudo = arquivo.read()

    # Extrair o número após o sinal de igual
    import re
    dia_atual = re.search(r'Dia atual do curso\s*=\s*(\d+)', conteudo)
    dia_atual = int(dia_atual.group(1))

    # Supondo que a coluna 'Dia' tem o número do dia e a coluna 'Ementa' tem a ementa correspondente
    ementa = planilha.loc[planilha['Dia do curso'] == dia_atual, 'Descrição da lição'].values

    texto_ementa = ementa[0]

    return texto_ementa


# Gerar lição com conteúdos coesos e organizados
def gerar_licao(texto_ementa):
     
    """
    Gera uma lição diária com base em uma ementa de estudo utilizando um modelo de linguagem natural.

    Esta função recebe a ementa de um curso, e utiliza um modelo de linguagem para gerar uma lição estruturada 
    seguindo um template pré-definido. O conteúdo gerado é organizado em introdução, pontos principais, exemplos práticos 
    e uma questão reflexiva ao final.

    A lição é formatada para que possa ser lida em aproximadamente 10 a 15 minutos, com foco em clareza, progressão e facilidade de entendimento.

    Args:
        ementa_dia (list): Lista contendo o tópico do dia, extraído da ementa do curso.

    Returns:
        str: Uma string formatada contendo a lição gerada, estruturada com introdução, desenvolvimento, exemplos, 
        e uma questão reflexiva ao final.

    Template utilizado para a geração da lição:
        - Introduza o conceito de forma clara e objetiva.
        - Detalhe os pontos principais, incluindo exemplos práticos quando aplicável.
        - Inclua análises curtas de obras ou textos relevantes.
        - Finalize com uma pergunta reflexiva ou sugestão de exercício prático.
        - Tamanho: Aproximadamente 10 a 15 minutos de leitura.

    Exemplo de uso:
        licao = gerar_licao(['Biografia de Jung, sua formação e influências'])
        print(licao)
    """
    
    ## Configuração do Template
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
    response = chain.invoke(texto_ementa)

    # Formata a resposta, adicionando uma linha em branco após cada nova linha para melhorar a legibilidade
    formatted_response = response.replace("\n", "\n\n")

    # Imprime a resposta formatada
    return formatted_response

# Enviar lição por WhatsApp

def enviar_licao_por_whatsapp(licao):
    
    """
    Envia a lição gerada por WhatsApp utilizando a API do Twilio.

    Args:
        licao (str): A lição gerada, contendo o texto a ser enviado.

    Returns:
        None
    """

    # Número de WhatsApp de destino
    
    
    to_whatsapp_number = "+553184483183"  # Substitua pelo número de destino

    # Mensagem a ser enviada
    message_body = licao

    # enviar mensagem
    kit.sendwhatmsg_instantly(to_whatsapp_number, message_body)
    
    

# Executa a aplicação

path_to_ementa = 'data\\ementa_jung.xlsx'
path_txt_dia = 'data\\dia_curso.txt'

if __name__ == "__main__":
    ementa = extrair_ementa(path_to_ementa, path_txt_dia)
    licao = gerar_licao(ementa)
    print(licao)
    enviar_licao_por_whatsapp(licao)