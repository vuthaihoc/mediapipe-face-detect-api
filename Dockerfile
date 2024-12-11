# Sử dụng hình ảnh Python chính thức làm hình ảnh cơ sở
FROM python:3.12-slim

# Thiết lập thư mục làm việc
WORKDIR /app

# Sao chép file requirements.txt vào thư mục làm việc
COPY requirements.txt .

# Cài đặt các thư viện cần thiết
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install libgl1 libglib2.0-0 libsm6 libxrender1 libxext6 -y && rm -rf /var/lib/apt/lists/*

# Sao chép mã nguồn vào thư mục làm việc
COPY . .

# Mở cổng 5000
EXPOSE 5000

# Chạy ứng dụng Flask
CMD ["python", "app.py"]