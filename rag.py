from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
import re

# --- Custom Exception ---
# This exception is raised when no transcript is available for a given YouTube video.
class TranscriptUnavailableError(Exception):
    pass

# --- YouTube Study Assistant Class ---
class YoutubeStudyAssistant:
    def __init__(self):
        # Initialize instance variables
        self.video_id = ""  # Store the video ID
        self.transcript = ""  # Store the transcript text
        self.embeddings = None  # Store embeddings (vectorized text)
        self.vector_store = None  # Store the vector database (FAISS)
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)  # Initialize language model (GPT)

    # --- Extract YouTube Video ID ---
    def extract_video_id(self, url):
        """
        Extracts the video ID from a YouTube URL.
        
        Args:
            url (str): The YouTube video URL.

        Returns:
            str: The extracted video ID.
            
        Raises:
            ValueError: If the URL format is invalid.
        """
        match = re.search(r"(?:v=|youtu.be/)([\w-]{11})", url)  # Regex to extract video ID
        if match:
            return match.group(1)  # Return the extracted video ID
        else:
            raise ValueError("Invalid YouTube URL")  # Raise error if URL format is invalid

    # --- Retrieve Transcript ---
    def retrieve_transcript(self, youtube_video_id):
        """
        Retrieves the transcript for a given YouTube video.
        
        Args:
            youtube_video_id (str): The YouTube video ID.

        Raises:
            TranscriptUnavailableError: If the transcript is unavailable.
        """
        try:
            self.video_id = youtube_video_id  # Set the video ID
            # Fetch transcript in English
            transcript_list = YouTubeTranscriptApi.get_transcript(self.video_id, languages=["en"])
            # Join the transcript text from the chunks into one string
            self.transcript = " ".join(chunk["text"] for chunk in transcript_list)
        except (TranscriptsDisabled, NoTranscriptFound) as error:
            # Raise custom exception if transcript is unavailable
            raise TranscriptUnavailableError("No captions available for this video.") from error

    # --- Indexing the Transcript ---
    def indexing(self):
        """
        Index the transcript text for vector search using FAISS.
        This process splits the transcript into chunks and creates embeddings.
        """
        # Split the transcript into chunks for easier processing
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.create_documents([self.transcript])
        
        # Create embeddings for the transcript chunks
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        # Create a FAISS vector store from the chunks and embeddings
        self.vector_store = FAISS.from_documents(chunks, self.embeddings)

    # --- Retrieve Relevant Context ---
    def retriever(self, input_query):
        """
        Retrieves relevant documents based on the input query using similarity search.
        
        Args:
            input_query (str): The user's query to be answered.

        Returns:
            str: The context text based on the retrieved documents.
        """
        # Set up the retriever to search for the most similar documents
        retriever = self.vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})
        # Retrieve the relevant documents
        retrieved_docs = retriever.invoke(input_query)
        # Return the content of the retrieved documents
        return "\n\n".join(doc.page_content for doc in retrieved_docs)

    # --- Create Augmentation Prompt ---
    def augmentation_prompt(self):
        """
        Creates a prompt template for augmenting the assistant's response.
        
        Returns:
            PromptTemplate: The prompt template used for the RAG process.
        """
        return PromptTemplate(
            template="""
            You are a helpful assistant.
            Answer ONLY from the provided transcript context.
            You will be polite and treat the user as a student.
            You can explain about your data source and also reason your answer when asked for.
            If the context is insufficient, just say you don't know.

            {context}
            Question: {question}
            """,
            input_variables=['context', 'question']
        )

    # --- RAG Setup ---
    def RAG_setup(self, youtube_video_id):
        """
        Sets up the RAG (Retrieval-Augmented Generation) process by retrieving the transcript and indexing it.
        
        Args:
            youtube_video_id (str): The YouTube video ID.
        """
        self.retrieve_transcript(youtube_video_id)  # Retrieve transcript
        self.indexing()  # Index the transcript for vector search

    # --- RAG Process ---
    def RAG(self, input_query):
        """
        Handles the RAG process to answer the input query using the indexed transcript.
        
        Args:
            input_query (str): The user's query to be answered.

        Returns:
            str: The answer to the input query generated by the assistant.
        """
        context_text = self.retriever(input_query)  # Retrieve relevant context
        prompt = self.augmentation_prompt()  # Get the prompt template
        parser = StrOutputParser()  # Initialize the output parser

        # Set up parallel processing for the context and question
        parallel_chain = RunnableParallel({
            'context': RunnableLambda(lambda _: context_text),
            'question': RunnablePassthrough()
        })

        # Define the main chain of actions (parallel -> prompt -> LLM -> parser)
        main_chain = parallel_chain | prompt | self.llm | parser
        # Execute the chain and return the generated response
        return main_chain.invoke(input_query)

# --- Example Usage ---
# Create an instance of YoutubeStudyAssistant
# assistant = YoutubeStudyAssistant()
# assistant.RAG_setup("KTzGBJPuJwM")  # Set up the assistant with a YouTube video
# print(assistant.transcript)  # Print the transcript
# print(assistant.RAG(input_query="What is charge oscillation?"))  # Ask a question
# print(assistant.RAG("Can you summarize the video?"))  # Ask for a summary