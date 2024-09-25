from flask import Flask, request, jsonify, render_template_string, redirect, url_for
import hashlib
import time
import os
import threading
import codecs

app = Flask(__name__, static_folder='/opt/static')

SECRET_USER = "captain_hack_sparrow"
SECRET_PASS = "Unl34sh_Th3_Kr4k3n" 
TOKENS = {}

ais_active = False
flag = "ESD{Th3_Kr4ken}"
encrypted_flag = codecs.encode(flag, 'rot_13')
AIS_MESSAGE = f"FLAG:{encrypted_flag}\n"

def send_ais_message():
    global ais_active
    import socket
    print("test IP SERVEUR : ", os.getenv("SERVER_IP", "127.0.0.1"))
    SERVER_IP = "172.28.26.130"  # Adresse IP de la machine hôte.
    SERVER_PORT = 12345
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while ais_active:
        sock.sendto(AIS_MESSAGE.encode('utf-8'), (SERVER_IP, SERVER_PORT))
        print(f"Message AIS envoyé à {SERVER_IP}:{SERVER_PORT}")
        time.sleep(5)


@app.route('/')
def home():
    with open('/opt/ais_interface.html', 'r') as file:
        content = file.read()
    return render_template_string(content)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.is_json:
            data = request.json
            username = data.get('username')
            password = data.get('password')
        else:
            username = request.form.get('username')
            password = request.form.get('password')

        if username == SECRET_USER and password == SECRET_PASS:
            token = hashlib.sha256(f"{username}{time.time()}".encode()).hexdigest()
            TOKENS[token] = time.time() + 300  # Token valide pour 5 minutes
            if request.is_json:
                return jsonify({"token": token}), 200
            else:
                return f"Login successful. Your token is: {token}. \
                Ce token expire toute les 5 minutes. \
                Voir la page /view."
        
        if request.is_json:
            return jsonify({"error": "Invalid credentials"}), 401
        else:
            return "Invalid credentials", 401
    
    # Si c'est une requête GET, affichez le formulaire de login
    login_form = """
    <form method="post">
        <input type="text" name="username" placeholder="Username" required><br>
        <input type="password" name="password" placeholder="Password" required><br>
        <input type="submit" value="Login">
    </form>
    """
    return render_template_string(login_form)

@app.route('/check_token', methods=['POST'])
def check_token():
    if request.is_json:
        token = request.json.get('token')
    else:
        token = request.form.get('token')

    if token in TOKENS and TOKENS[token] > time.time():
        return jsonify({"valid": True}), 200
    return jsonify({"valid": False}), 401

@app.route('/view')
def view_file():
    filename = request.args.get('file', 'default.txt')
    filepath = os.path.join('/opt', filename)
    try:
        with open(filepath, 'r') as file:
            content = file.read()
        return content
    except IOError:
        return "Fichier non trouvé", 404
    
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory(app.static_folder, path)

@app.route('/start_ais', methods=['POST'])
def start_ais():
    global ais_active
    if request.is_json:
        token = request.json.get('token')
    else:
        token = request.form.get('token')

    if token in TOKENS and TOKENS[token] > time.time():
        if not ais_active:
            ais_active = True
            thread = threading.Thread(target=send_ais_message)
            thread.start()
        return jsonify({"message": "AIS messages started"}), 200
    else:
        return jsonify({"message": "Invalid token"}), 401


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)