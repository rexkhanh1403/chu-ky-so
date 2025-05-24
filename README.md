# Dự án chữ ký số -rexkhanh1403
# Ứng dụng Truyền File Chữ Ký Số An Toàn (Secure Digital Signature File Transfer App)

## 🌟 Giới thiệu

Ứng dụng "Truyền File Chữ Ký Số An Toàn" là một mô hình mô phỏng quá trình truyền dữ liệu bảo mật qua mạng TCP/IP. Mục tiêu chính là đảm bảo **tính toàn vẹn** và **tính xác thực** của file thông qua việc sử dụng **chữ ký số RSA**.

Ứng dụng sử dụng Python với Flask để xây dựng giao diện web thân thiện, kết hợp với Flask-SocketIO để giao tiếp thời gian thực, và thư viện `cryptography` để xử lý các tác vụ ký số và xác minh.

---

## ⚙️ Tính năng chính

- 🔐 Tạo và quản lý cặp khóa RSA tự động
- ✍️ Ký số file bằng thuật toán RSA kết hợp SHA-256
- ✅ Xác minh tính toàn vẹn và xác thực file
- 📤 Truyền file từ client tới server qua TCP socket
- 📥 Lưu file nhận được tại server nếu chữ ký hợp lệ
- 🌐 Giao diện web đơn giản, theo dõi nhật ký hoạt động thời gian thực
- 🧩 Hỗ trợ nhiều kết nối client đồng thời (server đa luồng)

---

## 📂 Cấu trúc thư mục

```plaintext
CHU_KY_SO/
├── client/
│   ├── app.py                 # Ứng dụng web Flask phía người gửi
│   ├── templates/
│   │   └── giao_dien.html     # Giao diện web đơn giản
│   ├── private_key.pem        # Khóa riêng để ký số
├── server/
│   ├── server.py              # Server TCP nhận và xác minh file
│   ├── public_key.pem         # Khóa công khai để xác minh chữ ký
│   ├── received_files/        # Thư mục lưu file đã xác minh
```

🛠️ Cơ chế hoạt động
1️⃣ Quản lý khóa
Khi chạy lần đầu, hệ thống sẽ tự tạo cặp khóa private_key.pem và public_key.pem nếu chưa tồn tại.

Khóa riêng dùng để ký, khóa công khai dùng để xác minh.

2️⃣ Ký và gửi file (client/app.py)
Người dùng chọn file từ giao diện web.

File được băm bằng SHA256, sau đó tạo chữ ký số bằng RSA.

File + chữ ký số được gửi qua socket tới server.

3️⃣ Nhận và xác minh (server/server.py)
Server nhận file và chữ ký số.

Băm lại file bằng SHA256.

Dùng public_key để xác minh chữ ký.

Nếu hợp lệ → lưu vào received_files/, in VALID.

Nếu không hợp lệ → báo lỗi, in INVALID.

🚀 Cài đặt
Yêu cầu:
Python 3.7 trở lên

pip

Cài thư viện cần thiết:
```
pip install Flask Flask-SocketIO cryptography Werkzeug

```
🎮 Hướng dẫn sử dụng
📁 Chuẩn bị:
Đảm bảo có các thư mục sau cùng cấp với server.py:

keys/: chứa public_key.pem

received_files/: nơi lưu file nhận được

▶️ Khởi động:
# 1. Mở 2 cửa sổ Terminal:

Server (chạy trước):
```
cd server
python server.py
```
Client (giao diện web):
```
cd client
python app.py
```
# 2. Truy cập trình duyệt:
```
http://127.0.0.1:5000/
```
# 3. Tại giao diện web:

Nhập IP + port server (mặc định: 127.0.0.1:8889)

Chọn file cần gửi

Nhấn Send File

# 4. Xem nhật ký log hiển thị:

Gửi file thành công

Kết quả xác minh: VALID hoặc INVALID

🔐 Bảo mật
Sử dụng thuật toán RSA 2048-bit

SHA-256 đảm bảo băm không trùng lặp

Chữ ký số đảm bảo:

Dữ liệu không bị thay đổi

Người gửi được xác thực

Server chỉ lưu file nếu xác minh hợp lệ

🧰 Công nghệ sử dụng
🔧 Backend:
Python

Flask (giao diện web)

Flask-SocketIO (giao tiếp real-time)

cryptography (tạo, ký và xác minh RSA)

socket, threading (server TCP đa luồng)

🎨 Frontend:
HTML5

JavaScript

Bootstrap (nếu dùng)

📄 License
This project is licensed under the MIT License – see the LICENSE file for details.
