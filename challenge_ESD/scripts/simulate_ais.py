import socket
import time
import requests
import codecs

# Définir l'adresse IP et le port du serveur AIS
SERVER_IP = "127.0.0.1"
SERVER_PORT = 12345

def get_token(username, password):
    response = requests.post('http://127.0.0.1/login', json={
        "username": username,
        "password": password
    })
    if response.status_code == 200:
        return response.json().get('token')
    return None

def check_token(token):
    response = requests.post('http://127.0.0.1/check_token', json={"token": token})
    return response.json().get('valid', False)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Exemple de message AIS au format NMEA
flag = "ESD{Fl4g_H3re}"
encrypted_flag = codecs.encode(flag, 'rot_13')
AIS_MESSAGE = f"FLAG:{encrypted_flag}"

# Créer une socket UDP pour envoyer des messages
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def send_ais_message():
    print("Début de l'envoi de messages AIS...", flush=True)
    while True:
        ais_message = AIS_MESSAGE
        sock.sendto(ais_message.encode('utf-8'), (SERVER_IP, SERVER_PORT))
        print(f"Message AIS envoyé à {SERVER_IP}:{SERVER_PORT}")
        time.sleep(5)

if __name__ == "__main__":    
    print("Script démarré.", flush=True) 
    send_ais_message()