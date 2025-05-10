from flask import Flask, request, jsonify
import subprocess
import json

app = Flask(__name__)

@app.route("/api/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    wallet = data.get("wallet_address")
    try:
        result = subprocess.run(
            ["python3", "risk_report.py", wallet],
            capture_output=True,
            text=True,
            check=True
        )
        output = json.loads(result.stdout)
        return jsonify(output)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
