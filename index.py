#Librerías
from flask import Flask, request #Permite crear los servicios web
import json #Permite formatear la información en la nomneclatura o formato json
from twilio.rest import Client # Permite mandar mensajes de texto
from sendgrid import SendGridAPIClient 
from sendgrid.helpers.mail import Mail
 
#Crea objeto Flask  - Permite crear todas las APIS
app = Flask(__name__)
 
#Se carga la informacion del archivo config.json
f = open("config.json", "r") #con open("config.json", "r") Se lee.
env = json.loads(f.read()) #con json.loads(f.read()) Se almacena dentro de una variable que se llama env
 
#Se crea el primer servicio web
@app.route('/test', methods=['GET'])
def test():
    return "hello world"

# Se crea un SERVICIO WEB en Flask (librería de Python para crear servicios web)
@app.route('/send_sms', methods=['POST']) # se crea con app.route y le colocamos un nombre (send_sms) y define el metodo POST
def send_sms():
    try:
        #Variables de configuracion
        account_sid = env['TWILIO_ACCOUNT_SID']
        auth_token = env['TWILIO_AUTH_TOKEN']
        origen = env['TWILIO_PHONE_NUMBER']#telefono origen de donde se enviarán los mensajes
        client = Client(account_sid, auth_token)#Se crea un cliente que envia el msj- hace la validación cta twilio(inicia sesión)
        #Captura los datos de la solicitud y los almacena en la variable data
        data = request.json
        contenido = data["contenido"]
        destino = data["destino"]
        #Envía el mensaje       
        message = client.messages.create(
                            body=contenido,
                            from_=origen,
                            to='+57' + destino
                        )
        print(message)
        return "send success"
    except Exception as e:
        print(e)
        return "error"

#Método de enviar correos
@app.route('/send_email', methods=['POST'])#Crea una ruta que se llama send_email bajo el método POST
def send_email():
    #Captura los datos de la solicitud
    data = request.json #Obtiene la información q se envia desde el cliente (postman)
    contenido = data["contenido"]
    destino = data["destino"]
    asunto = data["asunto"]
    print(contenido, destino, asunto)
    #Crea el mensaje a enviar
    message = Mail(
    from_email= env['SENDGRID_FROM_EMAIL'],
    to_emails= destino,
    subject= asunto,
    html_content= contenido)
    try:
        sg = SendGridAPIClient(env['SENDGRID_API_KEY'])
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
        return "send success"
    except Exception as e:
        print(e)
        return "error"

#Se ejecuta el servidor con la siguiente instrucción:
if __name__ == '__main__':
    app.run()