from flask import Flask, request, jsonify
from flask_cors import CORS
from models.parsers import PythonParser
import logging

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/test', methods=['GET'])
def test():
    return jsonify({'message': 'Backend is working!'}), 200

@app.route('/analyze', methods=['POST'])
def analyze_code():
    try:
        logger.debug("Received request to /analyze")
        data = request.get_json()
        
        if not data:
            logger.error("No JSON data received")
            return jsonify({
                'error': 'No se recibieron datos',
                'success': False
            }), 400
            
        code = data.get('code', '')
        if not code:
            logger.error("No code provided in request")
            return jsonify({
                'error': 'No se proporcionó código para analizar',
                'success': False
            }), 400
        
        logger.debug(f"Analyzing code: {code}")
        parser = PythonParser()
        graph = parser.parse(code)
        
        # Analizar la complejidad
        complexity = graph.get_overall_complexity()
        logger.debug(f"Calculated complexity: {complexity}")
        
        return jsonify({
            'complexity': complexity,
            'success': True
        })
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({
            'error': str(e),
            'success': False
        }), 400

if __name__ == '__main__':
    app.run(debug=True, port=3000, host='0.0.0.0')
