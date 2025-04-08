from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Set the base URL for your agent's submit endpoint
AGENT_SUBMIT_URL = "http://127.0.0.1:8000/submit"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send_checkin', methods=['POST'])
def send_checkin():
    # Get the data from the user input (pain level, mobility, etc.)
    type_ = request.form['type']
    pain_level = request.form['pain_level']
    mobility = request.form['mobility']
    medication = request.form['medication']

    # Construct the response message to send to the RecoveryCoachAgent
    response_message = {
        "type": type_,
        "pain_level": pain_level,
        "mobility": mobility,
        "medication": medication
    }

    # Send the message to the RecoveryCoachAgent
    try:
        res = requests.post(AGENT_SUBMIT_URL, json=response_message)
        if res.status_code == 200:
            return jsonify({"message": "Response sent successfully!"})
        else:
            return jsonify({"message": "Failed to send response."}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

