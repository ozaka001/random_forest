from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import joblib
import os

app = Flask(__name__,)
app.secret_key = 'your_secret_key'


# กำหนดเส้นทางของโมเดล
MODEL_PATH = "random_forest_model.pkl"
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
else:
    model = None

# Mapping คลาสเป็นชื่อสายงาน
job_mapping = {
    1: "programmer",
    2: "game&animation",
    3: "network",
    4: "embeded",
    5: "other"
}

@app.route('/')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', username=session['username'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == "admin" and password == "1234":
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return render_template('login.html', message="Invalid credentials. Please try again.")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Model not loaded. Please check the model file.'}), 500

    try:
        input_data = request.json.get('data')
        if not input_data or len(input_data) != 5:
            return jsonify({'error': 'Invalid input data. Please provide 5 numeric values.'}), 400

        prediction = model.predict([input_data])
        predicted_job = job_mapping.get(prediction[0], "Unknown")

        return jsonify({'Recommended Job': predicted_job})

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
