from flask import Flask, request, jsonify
import logging
import os

app = Flask(__name__)

# Configure logging for CloudWatch
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.route('/health', methods=['GET'])
def health():
    logger.info("Health check endpoint called")
    return jsonify({"status": "ok"}), 200

@app.route('/echo', methods=['POST'])
def echo():
    try:
        data = request.get_json()
        logger.info(f"Echo endpoint called with data: {data}")
        return jsonify(data), 200
    except Exception as e:
        logger.error(f"Error in echo endpoint: {str(e)}")
        return jsonify({"error": "Invalid JSON"}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)