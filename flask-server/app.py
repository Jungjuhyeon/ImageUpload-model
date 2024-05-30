import torchvision.models as models
import torchvision.transforms as transforms
import torch
from PIL import Image
from flask import Flask, jsonify, request
import requests
from io import BytesIO
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

# AI 모델 로드
model = torch.load('model_final.pth')
model.eval()

# 정규화 상수 수정
normalize_mean = [0.485, 0.456, 0.406]
normalize_std = [0.229, 0.224, 0.225]

# AI 모델 예측 결과 반환 함수
def get_prediction(image):
    # 이미지 처리 및 예측
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(normalize_mean, normalize_std),
    ])

    # 이미지가 RGB 모드가 아니면 변환
    if image.mode != 'RGB':
        image = image.convert('RGB')

    image = transform(image).unsqueeze(0)

    with torch.no_grad():
        outputs = model(image)
        _, preds = torch.max(outputs, 1)

    # 예측 클래스 가져오기
    class_names = ['abnormal', 'normal']  # 모델의 클래스 이름과 일치하게 수정
    class_idx = torch.argmax(outputs)
    class_name = class_names[int(class_idx.item())]  # 클래스 이름으로 변환
    data = {"result": class_name}
    return jsonify(data)

@app.route("/api/upload", methods=["POST"])
def index():
    image_url = request.json.get('fileUrl')

    if not image_url:
        return jsonify(error="No image URL provided"), 400

    try:
        # 이미지 URL에서 이미지 다운로드
        response = requests.get(image_url)
        response.raise_for_status()  # 요청이 성공했는지 확인
        image = Image.open(BytesIO(response.content))

        # 예측 결과 반환
        return get_prediction(image)
        
    except Exception as e:
        return jsonify(error=str(e)), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)