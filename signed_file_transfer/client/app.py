from flask import Flask, render_template, request, flash, redirect
import socket, os
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key

app = Flask(__name__)
app.secret_key = 'secret'  # Bạn có thể thay bằng một chuỗi mạnh hơn

HOST = '127.0.0.1'
PORT = 9999

# Load khóa riêng để ký file
try:
    with open("keys/private_key.pem", "rb") as f:
        private_key = load_pem_private_key(f.read(), password=None)
except FileNotFoundError:
    print("[LỖI] Không tìm thấy file private_key.pem")
    exit()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        uploaded_file = request.files.get("file")
        
        if uploaded_file and uploaded_file.filename:
            filename = uploaded_file.filename
            data = uploaded_file.read()

            # Tạo chữ ký số
            signature = private_key.sign(
                data,
                padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
                hashes.SHA256()
            )

            try:
                # Gửi file + chữ ký đến server
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((HOST, PORT))
                    s.sendall(filename.encode() + b"::" + signature + b"::" + data)

                flash("Gửi file thành công!", "success")
                print(f"[INFO] Đã gửi file: {filename}")
            except Exception as e:
                flash(f"Gửi thất bại: {e}", "danger")
                print(f"[LỖI] Không gửi được file: {e}")
            
            return redirect("/")

        else:
            flash("Vui lòng chọn một file để gửi.", "warning")
    
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
