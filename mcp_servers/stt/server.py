import os
from mcp.server.fastmcp import FastMCP
from google import genai
from google.genai import types

mcp = FastMCP("STT-Voice-Server")

@mcp.tool()
async def speech_to_text(audio_path: str) -> str:
    """Transcribe farmer audio queries into text using Gemini.

    Args:
        audio_path: Path to the audio file to transcribe.
    """
    if not os.path.exists(audio_path):
        return f"Error: Audio file {audio_path} not found."
        
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    client = None
    try:
        if api_key:
            client = genai.Client(api_key=api_key)
        else:
            client = genai.Client()
    except Exception as e:
        print(f"Warning: Could not initialize Google GenAI Client: {e}")
        
    if client:
        try:
            uploaded_file = client.files.upload(file=audio_path)
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[uploaded_file, "Transcribe this agricultural audio query verbatim."]
            )
            return response.text
        except Exception as e:
            return f"Error transcribing via Gemini: {e}"
            
    return "Farmer Query (Mocked): What is the best treatment for late blight on potatoes?"
