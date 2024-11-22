import grpc
from concurrent import futures
import time
from flask import Flask, request, jsonify
from ner_model import NERModel

import ner_pb2
import ner_pb2_grpc

# Load NER model
ner_model = NERModel()

# Flask app for REST API
app = Flask(__name__)

@app.route('/ner', methods=['POST'])
def rest_ner():
    data = request.get_json()
    text = data.get('text', '')
    if not text:
        return jsonify({'error': 'Text is required'}), 400

    # Perform NER
    result = ner_model.predict(text)
    return jsonify({'entities': result})


# gRPC server setup
class NerServicer(ner_pb2_grpc.NerServicer):
    def ExtractEntities(self, request, context):
        text = request.text
        entities = ner_model.predict(text)
        
        # Return NER results as gRPC response
        response = ner_pb2.NERResponse()
        for entity in entities:
            response.entities.add(text=entity['word'], label=entity['entity'])
        return response


def serve_grpc():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    ner_pb2_grpc.add_NerServicer_to_server(NerServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC server started on port 50051.")
    try:
        while True:
            time.sleep(86400)  # Keep the server running
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    # Run Flask app in a separate thread for REST API
    from threading import Thread
    rest_thread = Thread(target=lambda: app.run(debug=True, host='0.0.0.0', port=5000))
    rest_thread.start()

    # Start gRPC server
    serve_grpc()
