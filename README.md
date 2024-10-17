
# Pílulas de Conhecimento Diárias com Inteligência Artificial

## Descrição do Projeto

Este projeto é uma aplicação Python que utiliza a API da OpenAI para gerar e enviar lições diárias de um determinado tema escolhido pelo usuário. A aplicação propõe uma ementa de estudo, que é dividida em pequenas lições diárias. As lições são enviadas automaticamente por e-mail ou WhatsApp (via Twilio), proporcionando um aprendizado contínuo e de fácil consumo.

## Funcionalidades

- Geração de uma ementa de estudo com base no tema escolhido.
- Divisão da ementa em lições diárias curtas.
- Envio automático das lições via WhatsApp ou e-mail.
- Memória de lições enviadas para evitar repetições.
- Agendamento diário do envio das lições.

## Tecnologias Utilizadas

- **Python**
- **OpenAI API** para geração de conteúdo.
- **Twilio API** para envio de mensagens no WhatsApp.
- **SMTP** para envio de e-mails.
- **SQLite** para armazenamento local das lições enviadas.
- **APScheduler** para agendamento de tarefas.

## Como Configurar o Projeto

### Pré-requisitos

- **Python 3.x** instalado no sistema.
- Conta no **Twilio** (para envio de WhatsApp) ou acesso a um servidor SMTP (para envio de e-mails).
- Chave de API da **OpenAI**.

### Passos para Configuração

1. Clone o repositório:

   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio
   ```

2. Crie um ambiente virtual e ative-o:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate  # Windows
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Crie um arquivo `.env` com as seguintes variáveis de ambiente:

   ```bash
   OPENAI_API_KEY=your_openai_api_key
   TWILIO_ACCOUNT_SID=your_twilio_account_sid
   TWILIO_AUTH_TOKEN=your_twilio_auth_token
   TWILIO_WHATSAPP_NUMBER=whatsapp:+your_twilio_number
   SMTP_SERVER=smtp.yourprovider.com
   SMTP_PORT=your_smtp_port
   SMTP_USER=your_email_address
   SMTP_PASSWORD=your_email_password
   ```

5. Execute o script para testar a geração da ementa:

   ```bash
   python generate_ementa.py
   ```

6. Para iniciar o envio diário das lições, use o seguinte comando:

   ```bash
   python start_schedule.py
   ```

### Estrutura de Diretórios

```
.
├── LICENSE
├── README.md
├── .gitignore
├── .env.example
├── requirements.txt
├── generate_ementa.py
├── start_schedule.py
├── db/
│   └── licões.db  # Banco de dados SQLite com lições enviadas
└── utils/
    ├── openai_utils.py  # Funções para chamar a OpenAI API
    ├── twilio_utils.py  # Funções para envio via Twilio
    └── email_utils.py   # Funções para envio de e-mails
```

### Dependências

Liste as dependências em um arquivo `requirements.txt`. Exemplo:

```
openai
twilio
APScheduler
sqlite3
python-dotenv
```

### Como Contribuir

1. Fork o repositório.
2. Crie uma nova branch: `git checkout -b minha-feature`.
3. Faça as alterações necessárias e commit: `git commit -m 'Minha nova feature'`.
4. Envie para a branch original: `git push origin minha-feature`.
5. Crie uma pull request.

## Licença

Este projeto está licenciado sob a Licença MIT.
```

---
