import sys
import json
import joblib
import numpy as np
import os

def predict(data):
    try:
        model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
        model = joblib.load(model_path)
        
        input_data = np.array(data).reshape(1, -1)
        prediction = model.predict(input_data)[0]
        return {"Recommended Job": str(prediction)}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    input_data = json.loads(sys.argv[1])
    result = predict(input_data)
    print(json.dumps(result))
