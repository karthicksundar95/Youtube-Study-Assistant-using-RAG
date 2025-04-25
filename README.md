# YouTube Study Assistant using RAG LLM

Welcome to the **YouTube Study Assistant** project! This system integrates YouTube videos with the power of AI to help you learn and interact with video content through intelligent question answering. The application consists of a **Streamlit** front-end that interacts with a **Flask API** for building a knowledge base from YouTube transcripts and responding to queries.

---

## 🎯 Project Overview

The **YouTube Study Assistant** allows users to input YouTube URLs, extract video transcripts, and build a knowledge base that can be queried using AI. It leverages **Langchain** for building the RAG (Retrieval-Augmented Generation) pipeline, where the system retrieves relevant context from the transcript and uses **OpenAI GPT-4** to generate answers.

---

## 🔧 Tech Stack

Here’s the technology stack that powers this project:

- **Python** 🐍: The primary programming language.
- **Flask**: Web framework for building the backend API.
- **Streamlit**: Front-end framework to interact with the user in a visually appealing way.
- **Langchain**: Framework for managing language models and building the RAG pipeline.
- **OpenAI GPT-4**: Language model for generating responses.
- **YouTube Transcript API**: Extracts video transcripts.
- **FAISS**: Used to create the vector store for storing and querying transcript embeddings.
- **CORS**: Ensures communication between Streamlit (front-end) and Flask API (back-end).


---

## 🚀 User Journey

### 1. **Starting the Application**

To get started, make sure you have the following installed:
- Python (>= 3.8)
- Flask
- Streamlit
- OpenAI Python package
- Langchain
- YouTube Transcript API

Once everything is set up, run the following commands in your terminal to launch the back-end API and front-end interface:

**Start Flask API** (Backend)
   ```bash
   python api.py
   ```
### 2. **Interacting with the App**

Once the Flask API is up and running, proceed with the following steps to interact with the application.

**Start Streamlit App (Frontend)**

1. Open a new terminal window and run the following command to start the **Streamlit front-end**:

   ```bash
   streamlit run app.py

2. This will launch the Streamlit application and by default, it will be accessible at http://localhost:8501 on your browser.


3. Building the Knowledge Base
In the sidebar of the Streamlit app, you will find a text input box where you can paste a YouTube URL.

Enter the URL of a YouTube video. For example:

```bash
https://www.youtube.com/watch?v=KTzGBJPuJwM
```

After entering the URL, click the ⚙️ Build Knowledge Base button. This action sends the URL to the Flask API, which retrieves the transcript of the video and processes it to build a knowledge base.

4. Asking Questions
Once the knowledge base is built, you can ask any questions related to the video content.

You will see an input field titled "Ask a question:" below the knowledge base build button.

```bash
Type your question into the input field and press Enter.

For example, you can ask:

"What is charge oscillation?"

"Can you summarize the video?"

The system will use the extracted transcript and AI to generate answers.
```

5. View the Responses
After submitting your question, the system will process it and display the answer below the chat box.

The AI will generate a response based on the context from the video’s transcript.

6. Chat History
As you interact with the app, the conversation history will be maintained. Both your queries and the assistant’s responses will be visible in the chat interface, providing a seamless experience for continuous interaction.

---

## 🌟 Key Features

- **YouTube Video to Knowledge Base**  
  Extracts and indexes transcripts from YouTube videos automatically.

- **Querying**  
  Ask questions related to the video and get AI-powered answers based on the transcript.

- **AI-Powered Answers**  
  Uses **OpenAI GPT-4** to generate responses using Retrieval-Augmented Generation (RAG).

- **Fast Setup**  
  Paste a URL and start interacting — no need to upload videos or transcripts manually.

- **Cross-Origin Support**  
  CORS is enabled to support smooth communication between Streamlit (frontend) and Flask (backend).

---

## 🛠️ Tech Stack

- **Frontend**:  
  - Streamlit  
  - React (via Streamlit's underlying components)

- **Backend**:  
  - Flask  
  - Python  
  - CORS for cross-origin support

- **AI & NLP**:  
  - OpenAI GPT-4  
  - FAISS for similarity search  
  - YouTube Transcript API for caption retrieval

---
## 📁 Folder Structure

```
YouTube-Study-Assistant/ 
    ├── app.py # 🎨 Streamlit frontend for user  interaction 
    ├── api.py # 🛠️ Flask backend exposing RAG endpoints 
    ├── rag.py # 🧠 Core logic: YouTube transcript parsing & retrieval-augmented generation 
    ├── requirements.txt # 📦 Python dependencies 
    └── README.md # 📄 Project documentation
    |__ dockerfile # docker file with instructions
    |__ start.h # executable function to run the apps in docker
```
## 📦 Installation & Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/karthicksundar95/Youtube-Study-Assistant-using-RAG.git
   cd YouTube-Study-Assistant
2. Create virtual environment and activate:

```bash

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Start Flask API:

```bash
python api.py
```

5. Start Streamlit App:

In a new terminal:

```bash
streamlit run app.py
```

Open your browser and navigate to http://localhost:8501.

## 🐳 Docker Support

You can run the entire YouTube Study Assistant (Flask API + Streamlit app) in isolated containers using Docker. This is ideal for easy deployment and avoiding dependency issues.

### 📦 Docker Overview

We use Docker to:
- Run the Flask API backend  
- Run the Streamlit frontend  
- Easily share or deploy the app across systems  

### 🧱 Dockerfile

Ensure your project root contains a `Dockerfile` like this:

```dockerfile
# Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=api.py
ENV STREAMLIT_SERVER_PORT=8501

EXPOSE 5050
EXPOSE 8501

CMD ["bash", "start.sh"]
```

## Start.sh
This script starts both the Flask API and the Streamlit frontend.
```
#!/bin/bash
# start.sh

# Start the Flask API in the background
python api.py &

# Start the Streamlit frontend
streamlit run app.py --server.port 8501
```
Make sure it’s executable:
```chmod +x start.sh```

### 🛠️ How to Run with Docker

You can easily run the entire project inside a Docker container without installing Python or dependencies manually.

#### 1. 🏗️ Build the Docker Image

From the root directory of the project, run the following command:

```bash
docker build -t yt-study-assistant .
```

This command will:

Copy your project files into the image

Install all required dependencies from requirements.txt

Expose ports for the Flask backend and Streamlit frontend

Set up a container that runs both services

### 🚀 Run the Container
Make sure you have your OpenAI API Key available. Then run:

```
docker run -p 8501:8501 -p 5050:5050 -e OPENAI_API_KEY="your_openai_key" yt-study-assistant
```
This will:

- Expose port 8501 for the Streamlit frontend

- Expose port 5050 for the Flask backend

- Pass your API key securely as an environment variable

You can now access the app in your browser at:
http://localhost:8501

### 🔁 Verify the App
Go to http://localhost:8501

Paste a YouTube video link in the sidebar and click Build Knowledge Base

Ask questions about the video using the chat interface

## 🛠️ Troubleshooting Guide

### 1. ❗ Port 5000/5050 Already in Use

**Issue:**  
When running `api.py`, you may see:
```
Address already in use. Port 5000 is in use by another program.
```

**Solution:**  
Identify and kill the process using the port:
```bash
lsof -i :5000
kill -9 <PID>
```

**macOS Tip:**  
If port 5000 is in use due to AirPlay:
- Go to **System Preferences → General → AirDrop & Handoff**
- **Disable AirPlay Receiver**

---

### 2. 🌐 Streamlit Fails to Fetch from Flask API

**Issue:**  
The frontend does not receive responses from the Flask backend.

**Solution:**  
Ensure CORS is correctly configured in `api.py`:
```python
from flask_cors import CORS
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
```

Also ensure both servers are running:
- `api.py` on port 5050 (backend)
- `app.py` on Streamlit’s default port (frontend)

---

### 3. 📼 Transcript Not Found Error

**Issue:**
```
Transcript not available
```

**Cause:**  
- Captions might be disabled
- No English transcript available

**Fix:**  
Use a video with **enabled English subtitles**.

---

### 4. 🔄 Changes Not Reflecting

**Cause:**  
Cached content or outdated server state.

**Solution:**  
- Restart both `api.py` and `app.py`
- Clear your browser cache and try again

---

### 5. ⚠️ Error: Knowledge Base Not Built Yet

**Issue:**  
You tried querying before clicking **Build Knowledge Base**.

**Fix:**  
- Always **click the ⚙️ Build Knowledge Base** button **first** from the sidebar
- Then start asking questions

---
## 🙌 Contributions

We welcome contributions of all kinds to enhance this project further!

### Ways You Can Contribute:
- 🐞 **Report Bugs**: Found a glitch or edge case? Let us know via issues!
- 🧠 **Improve Prompts**: Craft better, more instructive prompts to make the assistant smarter.
- ✨ **Feature Requests**: Got an idea? We'd love to hear how you'd expand this.
- 🧪 **Testing**: Try the app with diverse YouTube videos and queries.
- 📦 **Deployment Help**: Add Docker support, cloud deployment instructions, or CI/CD setups.

### To Get Started:
1. Fork the repo 🍴
2. Create a new branch: `git checkout -b my-feature`
3. Commit your changes: `git commit -m 'Add new feature'`
4. Push to the branch: `git push origin my-feature`
5. Open a Pull Request! 🔁

We follow the [Conventional Commits](https://www.conventionalcommits.org/) format and maintain a friendly, inclusive community 🫱🏽‍🫲🏼

---

## 🎯 Conclusion

This project transforms passive video consumption into **active learning** using the power of AI 🔍💬.

By embedding the transcript, generating context-aware responses, and offering a friendly assistant interface, it simplifies concept discovery from complex YouTube videos — just like a study buddy who never gets tired!

Whether you're:
- A student 🧑‍🎓 revising for exams
- A curious learner 💡
- Or a developer exploring RAG pipelines 🛠️

### Flow Chart (Psuedo code)
[Psuedo code flow chart](./code2flow_wKpduY.svg)
