# JStar Backend

## Yêu cầu

- **Python 3.12** - [Tải về](https://www.python.org/downloads/)
- **pip** hoặc **conda**

---

## 🚀 Cài đặt

### Cách 1: Dùng venv (khuyên dùng)

```bash
# Tạo môi trường ảo
python -m venv venv

# Kích hoạt (Windows)
venv\Scripts\activate

# Kích hoạt (macOS/Linux)
source venv/bin/activate

# Cài đặt thư viện
pip install -r requirements.txt
```

### Cách 2: Dùng Conda

```bash
# Tạo môi trường conda
conda create -n jstar python=3.12

# Kích hoạt
conda activate jstar

# Cài đặt thư viện
pip install -r requirements.txt
```

---

## ▶️ Chạy Server

```bash
uvicorn app.main:app --reload
```
Mở: http://localhost:8000

---

## 📁 Cấu trúc dự án

```
temp_backend/
├── app/
│   ├── __init__.py
│   └── main.py       # ← Toàn bộ code ở đây
├── requirements.txt
└── README.md
```

---

## 📖 API Specification

### POST /api/chart

**Request:**
```json
{
  "name": "Nguyễn Văn A",
  "date": "1990-06-15",
  "time": "14:30",
  "city": "Hanoi",
  "country": "Vietnam"
}
```

**Response:** Dữ liệu bản đồ sao (planets, houses, aspects, angles)

