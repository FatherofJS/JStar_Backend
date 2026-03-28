# 🛠️ JStar Backend - The Cosmic Engine 🛠️

**JStar Backend** là "bộ não" xử lý toàn bộ dữ liệu thiên văn và trí tuệ nhân tạo của hệ thống JStar. Được xây dựng trên nền tảng **FastAPI (Python 3.12)**, hệ thống đảm bảo tốc độ phản hồi cực nhanh cho các phép tính hành tinh phức tạp và tương tác AI thời gian thực.

---

## 🚀 Tính Năng 

### 1. Tính Toán Thiên Văn 
- Sử dụng engine **Kerykeion** (dựa trên Swiss Ephemeris) để tính toán vị trí hành tinh với độ chính xác tuyệt đối.
- Hỗ trợ đầy đủ 12 nhà (Houses), 10 hành tinh chính, Chiron, và các điểm nút (North/South Node).
- Hệ thống Aspect Grid tự động tính toán 5 góc chiếu chính (Conjunction, Opposition, Square, Trine, Sextile).

### 2. 🤖 Trợ Lý Tâm Linh (AI Interpretation)
- Tích hợp **Groq SDK** với các mô hình **Llama 3.3 70B** và **Llama 3.1 8B**.
- Hệ thống **Multi-API Key Rotation** giúp vượt qua giới hạn Rate Limit của nhà cung cấp.
- Persona độc bản: Sarcastic, Gen-Z, và luôn nói sự thật trần trụi dựa trên dữ liệu lá số thực.

### 3. 🖼️ Quản Lý  (Cloudinary)
- Tự động hóa việc truy xuất và phân loại hàng ngàn hình ảnh từ Cloudinary cho tính năng Aesthetic Board.
- Hệ thống lọc thông minh theo Cung hoàng đạo (Zodiac) và Thể loại (Category: Fashion, Objects, etc.).

--
## � Tech Stack & Công Cụ

| Thành phần | Công nghệ |
| --- | --- |
| **Ngôn ngữ** | Python 3.12+ |
| **Framework** | FastAPI |
| **Dữ liệu Chiêm tinh** | Kerykeion & Swiss Ephemeris |
| **AI Processing** | Groq Cloud (Llama 3 models) |
| **Rate Limiter** | SlowAPI (Resource protection) |
| **Image Hosting** | Cloudinary API |

---

##  Cài Đặt & Triển Khai (Setup)

### 1. Môi trường Python
```bash
# Tạo môi trường ảo
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate

# Cài đặt dependencies
pip install -r requirements.txt
```

### 2. Biến Môi Trường (.env)
Tạo file `.env` với các tham số sau:
- `GROQ_API_KEYS`: Danh sách key API Groq (phân tách bởi dấu phẩy).
- `CLOUDINARY_BOARD_CLOUD_NAME`, `API_KEY`, `API_SECRET`: Key từ Cloudinary.
- `FRONTEND_URL`: Danh sách URL frontend (với CORS).

### 3. Khởi chạy
```bash
uvicorn app.main:app --reload
```
Tài liệu API tương tác tại: `http://localhost:8000/docs`

---
© 2026 **FatherOfJS Team**. Đưa sức mạnh của các vì sao vào từng dòng code
