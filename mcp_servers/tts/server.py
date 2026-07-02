import os

from google import genai
from google.genai import types
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("TTS-Voice-Server")

@mcp.tool()
async def text_to_speech(text: str, output_path: str) -> str:
    """Generate audio feedback for the farmer from text.

    Args:
        text: Text to synthesize.
        output_path: Path to save the output audio file (e.g. 'speech.mp3').
    """
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
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=f"Read this text out loud verbatim: {text}",
                config=types.GenerateContentConfig(
                    response_modalities=["AUDIO"]
                )
            )

            audio_bytes = None
            for part in response.candidates[0].content.parts:
                if part.inline_data and part.inline_data.mime_type.startswith("audio/"):
                    audio_bytes = part.inline_data.data
                    break

            if audio_bytes:
                os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
                with open(output_path, "wb") as f:
                    f.write(audio_bytes)
                return f"Successfully generated Gemini Speech audio file at: {output_path}"
        except Exception as e:
            print(f"Gemini Audio Generation failed: {e}. Falling back to gTTS.")

    try:
        from gtts import gTTS
        tts = gTTS(text=text, lang='en')
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        tts.save(output_path)
        return f"Generated speech audio file via gTTS at: {output_path}"
    except Exception:
        txt_path = output_path + ".txt"
        os.makedirs(os.path.dirname(os.path.abspath(txt_path)), exist_ok=True)
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(f"[AUDIO TRANSCRIPT]: {text}")
        return f"Warning: Both Gemini and gTTS failed. Mock transcript saved to: {txt_path}"
