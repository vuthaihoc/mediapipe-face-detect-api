from flask import Flask, request, jsonify, send_file
import cv2
import mediapipe as mp
import numpy as np
import os
import io

app = Flask(__name__)

# Lấy giá trị từ biến môi trường, với giá trị mặc định nếu không có
min_detection_confidence = float(os.getenv('MIN_DETECTION_CONFIDENCE', 0.5))
model_selection = int(os.getenv('MODEL_SELECTION', 1))

# Khởi tạo MediaPipe Face Detection
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=min_detection_confidence, model_selection=model_selection)

@app.route('/detect_face', methods=['POST'])
def detect_face():
    # Kiểm tra xem có file được gửi lên không
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Đọc ảnh từ file
    img_array = np.frombuffer(file.read(), np.uint8)
    image = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    # Chuyển đổi ảnh sang RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Phát hiện mặt
    results = face_detection.process(image_rgb)

    faces = []
    if results.detections:
        for detection in results.detections:
            bboxC = detection.location_data.relative_bounding_box
            confidence = detection.score[0]
            h, w, _ = image.shape
            x, y, width, height = int(bboxC.xmin * w), int(bboxC.ymin * h), int(bboxC.width * w), int(bboxC.height * h)
            faces.append({
                'bounding_box': {
                    'x': x,
                    'y': y,
                    'width': width,
                    'height': height
                },
                'confidence': float(confidence)
            })
            # Vẽ hình chữ nhật quanh khuôn mặt
            cv2.rectangle(image, (x, y), (x + width, y + height), (255, 0, 0), 2)
            # Hiển thị confidence bên cạnh hình chữ nhật
            cv2.putText(image, f'{confidence:.2f}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    # Kiểm tra tham số query
    return_image = request.args.get('return_image', 'false').lower() == 'true'

    if return_image:
        # Chuyển đổi hình ảnh đã đánh dấu thành định dạng JPEG và lưu vào bộ nhớ
        _, buffer = cv2.imencode('.jpg', image)
        img_bytes = io.BytesIO(buffer)
        return send_file(img_bytes, mimetype='image/jpeg')

    return jsonify({'faces': faces})

if __name__ == '__main__':
    # Lấy PORT từ biến môi trường, nếu không có thì mặc định là 5000
    port = int(os.environ.get('PORT', 5000))
    debug = bool(os.environ.get('DEBUG', False))
    app.run(host='0.0.0.0', port=port, debug=debug)