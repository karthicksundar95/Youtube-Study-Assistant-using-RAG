from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import sys
from rag import YoutubeStudyAssistant, TranscriptUnavailableError

app = Flask(__name__)

# --- CORS Configuration ---
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# --- Logging setup ---
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

assistant = YoutubeStudyAssistant()
logging.info("API Initialized")

@app.route("/build", methods=["POST"])
def build():
    logging.info("Inside /build endpoint")
    data = request.get_json(force=True)
    youtube_url = data.get("url", "")
    logging.info(f"Received YouTube URL: {youtube_url}")

    try:
        video_id = assistant.extract_video_id(youtube_url)
        if not video_id:
            logging.warning("Invalid YouTube URL format")
            return jsonify({"error": "Invalid YouTube URL"}), 400

        assistant.RAG_setup(video_id)
        logging.info("RAG setup completed successfully")
        return jsonify({"message": "Knowledge base built successfully"}), 200

    except TranscriptUnavailableError:
        logging.warning("Transcript unavailable for the given video")
        return jsonify({"error": "Transcript not available"}), 404
    except Exception as e:
        logging.error(f"Exception during build: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/query", methods=["POST"])
def query():
    logging.info("Inside /query endpoint")
    data = request.get_json(force=True)
    user_query = data.get("query", "")
    logging.info(f"Received query: {user_query}")

    if not assistant.vector_store:
        logging.warning("Query attempted before building knowledge base")
        return jsonify({"error": "Knowledge base not built yet."}), 400

    try:
        answer = assistant.RAG(user_query)
        logging.info(f"Generated answer: {answer}")
        return jsonify({"response": answer}), 200
    except Exception as e:
        logging.error(f"Exception during query: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
