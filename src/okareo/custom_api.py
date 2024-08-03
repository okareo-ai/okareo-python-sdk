from flask import Flask
from flask import request, jsonify
import subprocess
import logging
import os
import signal

def create_app(custom_model):
    app = Flask(__name__)
    app.config['model'] = custom_model

    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    # chat completion
    # @app.route("/v1//chat/completions", methods=["POST", "GET"])
    @app.route("/chat/completions", methods=["POST"])
    def chat_completion():
        data = request.json

        messages = data["messages"]
        return custom_model.invoke(messages).model_prediction

    @app.route('/shutdown', methods=['GET'])
    def stopServer():
        os.kill(os.getpid(), signal.SIGINT)
        return jsonify({ "success": True, "message": "Server is shutting down..." })
    
    return app