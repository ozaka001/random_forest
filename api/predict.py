from http.server import BaseHTTPRequestHandler
import json
import joblib
import numpy as np
import os

def load_model():
    try:
        model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
        return joblib.load(model_path)
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

model = load_model()

def predict(data):
    if model is None:
        return {"error": "Model not loaded"}
    try:
        input_data = np.array(data).reshape(1, -1)
        prediction = model.predict(input_data)[0]
        return {"Recommended Job": str(prediction)}
    except Exception as e:
        return {"error": str(e)}

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            
            result = predict(data['data'])
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
