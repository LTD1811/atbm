# 🛡️ Quiz An Toàn Bảo Mật

Ứng dụng quiz trắc nghiệm về An Toàn Bảo Mật thông tin, được xây dựng bằng FastAPI.

## 📋 Yêu cầu

- **Python 3.13+**
- **uv** (Python package manager)

Cài đặt uv:

pip install uv


## 🚀 Cài đặt và Chạy

### 1. Clone repository

```bash
git clone https://github.com/LTD1811/atbm.git
cd atbm
```

### 2. Cài đặt dependencies

```bash
uv sync
```

### 3. Chạy ứng dụng

```bash
uv run uvicorn app.main:app --reload
```

### 4. Mở trình duyệt

Truy cập: **http://127.0.0.1:8000**

## 🎮 Tính năng

- **📚 Chế độ Luyện tập**: Làm bài theo khoảng câu hỏi (1-50, 51-100, ...)
- **🎲 Chế độ Ngẫu nhiên**: Random 10, 20, hoặc 50 câu
- **📝 Trắc nghiệm**: Câu hỏi có 4 đáp án A/B/C/D
- **📖 Flashcard**: Câu hỏi tự luận với đáp án ẩn


