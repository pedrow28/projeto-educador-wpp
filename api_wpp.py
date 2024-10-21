import os
from twilio.rest import Client
from dotenv import load_dotenv

# Carregar variáveis do arquivo .env
load_dotenv()

# Credenciais do Twilio
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
twilio_whatsapp_number = os.getenv('TWILIO_WHATSAPP_NUMBER')

# Número de WhatsApp de destino
to_whatsapp_number = 'whatsapp:+553184483183'  # Substitua pelo número de destino

# Mensagem a ser enviada
message_body = 'Olá! Esta é uma mensagem enviada pelo Twilio WhatsApp API!'

# Configurar cliente Twilio
client = Client(account_sid, auth_token)

# Enviar mensagem
message = client.messages.create(
    body=message_body,
    from_=twilio_whatsapp_number,
    to=to_whatsapp_number
)

print(f"Mensagem enviada com SID: {message.sid}")
