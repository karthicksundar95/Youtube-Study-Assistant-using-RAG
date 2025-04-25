FROM python:3.11

WORKDIR /youtube_study_assistant

COPY . /youtube_study_assistant

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5050
EXPOSE 8501

RUN chmod +x start.sh

CMD ["./start.sh"]
