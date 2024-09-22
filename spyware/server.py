from flask import Flask, request
import os

app = Flask(__name__)

# 파일 업로드를 위한 경로 설정
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/upload', methods=['POST'])
def upload():
    data = request.form
    print("Data received:", data)

    # 파일 저장
    if 'file' in request.files:
        file = request.files['file']
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        print(f"File saved to: {filepath}")

    return "Data received", 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
