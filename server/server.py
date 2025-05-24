import socket
import os
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_public_key

HOST = "127.0.0.1"
PORT = 9999

with open("backend/keys/public.pem", "rb") as f:
    pub_key = load_pem_public_key(f.read())

os.makedirs("downloads", exist_ok=True)

with socket.socket() as server:
    server.bind((HOST, PORT))
    server.listen(1)
    print(f"🟢 Đang lắng nghe tại {HOST}:{PORT}...")

    while True:
        client, addr = server.accept()
        print(f"🔗 Kết nối từ {addr}")
        data = b""
        while b"::" not in data:
            data += client.recv(1024)
        name, data = data.split(b"::", 1)
        name = name.decode()

        while b"::" not in data:
            data += client.recv(1024)
        sign, filedata = data.split(b"::", 1)
        while True:
            part = client.recv(4096)
            if not part:
                break
            filedata += part

        try:
            pub_key.verify(
                sign,
                filedata,
                padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
                hashes.SHA256()
            )
            with open(f"downloads/{name}", "wb") as f:
                f.write(filedata)
            print(f"{name}' đã nhận và xác minh.")
        except Exception as err:
            print(f"Chữ ký không hợp lệ: {err}")

        client.close()
