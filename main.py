from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import HumanMessage # Import HumanMessage for direct use

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Read the API key from environment
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize FastAPI app
app = FastAPI() 

# Initialize Chat Model with API key
# Ensure model_name is correct, e.g., "gpt-3.5-turbo" or "gpt-4o"
chat_model = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=openai_api_key)

# ---

### Request Body Schema
class ChatRequest(BaseModel):
    """
    Schema for the incoming chat request, expecting a 'message' string.
    """
    message: str

# ---

### Root Route
@app.get("/")
def read_root():
    """
    Root endpoint to confirm the chatbot service is running.
    """
    return {"message": "🚀 LangChain Chatbot is running!"}

# ---

### Simple Chat Route
@app.post("/chat")
async def simple_chat(request: ChatRequest):
    """
    Handles a simple chat request, sending the user's message directly to the
    ChatOpenAI model and returning its response.
    """
    try:
        user_message = request.message
        # Send the user's message as a HumanMessage directly to the chat model
        response = chat_model([HumanMessage(content=user_message)])
        return {"response": response.content}
    except Exception as e:
        # Catch any exceptions during the process and return an HTTP 500 error
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")