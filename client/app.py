from flask import Flask, render_template, request, redirect, flash
import socket
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.serialization import load_pem_private_key

app = Flask(__name__)
app.secret_key = "new_secret"

SERVER_IP = "127.0.0.1"
SERVER_PORT = 9999

with open("backend/keys/private.pem", "rb") as key_file:
    secret_key = load_pem_private_key(key_file.read(), password=None)

@app.route("/", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        f = request.files["file"]
        if f:
            data = f.read()
            signed = secret_key.sign(
                data,
                padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
                hashes.SHA256()
            )
            try:
                with socket.socket() as sock:
                    sock.connect((SERVER_IP, SERVER_PORT))
                    sock.sendall(f.filename.encode() + b"::" + signed + b"::" + data)
                flash("Gửi file thành công!", "success")
            except Exception as e:
                flash(f"Lỗi khi gửi: {e}", "danger")
        return redirect("/")
    return render_template("upload_page.html")

if __name__ == "__main__":
    app.run(debug=True)
