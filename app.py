from flask import Flask, render_template, request, redirect, url_for
import openai
import requests
from google.cloud import texttospeech
from pydub import AudioSegment
import gender_guesser.detector as gender
import os
import socket
from werkzeug.utils import secure_filename

# Define paths inside static
PODCAST_DIR = "static/podcast/"
TEXT_DIR = os.path.join(PODCAST_DIR, "texts/")
AUDIO_DIR = os.path.join(PODCAST_DIR, "audio/")

# Ensure directories exist
os.makedirs(TEXT_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)

from dotenv import load_dotenv


# Load environment variables from .env
load_dotenv()

# Set API keys
openai.api_key = os.getenv("OPENAI_API_KEY")
serp_api_key = os.getenv("SERP_API_KEY")

# Set Google Cloud Credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")



app = Flask(__name__)

# Initialize the gender detector
detector = gender.Detector()

# Supported languages (limited to English for now)
supported_languages = {
    "English": "english"
}

# Function to fetch news from Google News API via SerpApi
def fetch_google_news(news_type):
    api_url = f"https://serpapi.com/search.json?engine=google_news&q={news_type}&api_key={serp_api_key}"
    response = requests.get(api_url)
    
    if response.status_code == 200:
        news_data = response.json()
        articles = news_data.get("news_results", [])
        
        # Extract titles and summaries
        news_items = []
        for article in articles[:5]:  # Limit to top 5 articles
            title = article.get("title", "No title available")
            summary = article.get("snippet", "No summary available")
            news_items.append(f"{title}: {summary}")
        
        return news_items
    else:
        return []

# Function to generate podcast conversation
def generate_conversation(guest_name, host_name, news_titles, news_type):
    if not news_titles:
        return "Sorry, no news available at the moment."

    # Create conversation starter template
    conversation_prompt = f"""
    Create a 10-minute {news_type} podcast conversation between {host_name} (the host) and {guest_name} (the guest) for the AI Amplified podcast.
    Structure the conversation in a clear dialogue format where each speaker is labeled with either "Host:" or "Guest:". 
    For example:
    {host_name}: [Host's dialogue]
    {guest_name}: [Guest's dialogue]
    {host_name}: [Host's dialogue]

    Begin the conversation with a stunning welcome from the host, followed by an engaging response from the guest.
    Use the latest news data to guide the dialogue. Discuss the following news headlines:
       - "{news_titles[0]}"
       - "{news_titles[1]}"
       - "{news_titles[2]}"
       - "{news_titles[3]}"
       - "{news_titles[4]}"
    The tone, emotion, and flow should adapt naturally based on the genre, ensuring a dynamic, human-like exchange in {supported_languages}.
    """


    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": f"You are an AI podcast host named {host_name}."},
            {"role": "user", "content": conversation_prompt}
        ]
    )

    generated_conversation = response['choices'][0]['message']['content'].strip()
    generated_conversation = generated_conversation.replace("[Opening Music]", "").replace("[Ending Music]", "").replace("**", "")

    return generated_conversation

# Assign voice based on detected gender
def assign_voice_by_gender(name):
    gender_result = detector.get_gender(name.split()[0])
    if gender_result in ["male", "mostly_male"]:
        return texttospeech.SsmlVoiceGender.MALE
    elif gender_result in ["female", "mostly_female"]:
        return texttospeech.SsmlVoiceGender.FEMALE
    else:
        return texttospeech.SsmlVoiceGender.NEUTRAL

# Convert text to audio using Google Cloud Text-to-Speech
def text_to_audio(conversation, host_name, guest_name, audio_path):
    client = texttospeech.TextToSpeechClient()
    
    host_voice_gender = assign_voice_by_gender(host_name)
    guest_voice_gender = assign_voice_by_gender(guest_name)

    host_voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=host_voice_gender
    )
    guest_voice = texttospeech.VoiceSelectionParams(
        language_code="en-GB",
        ssml_gender=guest_voice_gender
    )

    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

    lines = conversation.split('\n')
    audio_clips = []
    silence = AudioSegment.silent(duration=500)

    for line in lines:
        if line.strip().startswith(host_name):
            text = line.replace(f"{host_name}: ", "")
            synthesis_input = texttospeech.SynthesisInput(text=text)
            response = client.synthesize_speech(input=synthesis_input, voice=host_voice, audio_config=audio_config)
        elif line.strip().startswith(guest_name):
            text = line.replace(f"{guest_name}: ", "")
            synthesis_input = texttospeech.SynthesisInput(text=text)
            response = client.synthesize_speech(input=synthesis_input, voice=guest_voice, audio_config=audio_config)
        else:
            continue

        temp_audio_path = "temp_audio.mp3"
        with open(temp_audio_path, "wb") as out:
            out.write(response.audio_content)

        audio_clip = AudioSegment.from_mp3(temp_audio_path)
        audio_clips.append(audio_clip + silence)

    combined_audio = sum(audio_clips) if audio_clips else AudioSegment.silent(duration=1000)
    
    # Save audio inside static/podcast/audio/
    combined_audio.export(audio_path, format="mp3")

    if os.path.exists(temp_audio_path):
        os.remove(temp_audio_path)


# Landing page route
@app.route('/')
def landing_page():
    return render_template('landing.html')

# Generate conversation page route
@app.route('/generate', methods=['GET', 'POST'])
def generate_page():
    if request.method == 'POST':
        guest_name = request.form.get('guest_name', '').strip()
        host_name = request.form.get('host_name', '').strip()
        news_type = request.form.get('news_type', '').strip().replace(" ", "_")  # Remove spaces
        
        # Fetch news and generate conversation
        news_titles = fetch_google_news(news_type)
        generated_conversation = generate_conversation(guest_name, host_name, news_titles, news_type)
        
        # Create a secure filename
        filename = f"{host_name}_{guest_name}_{news_type}.txt"
        file_path = os.path.join(TEXT_DIR, filename)

        # Save conversation to a text file inside static/podcast/texts/
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(generated_conversation)

        # Read the stored text to pass it to the template
        with open(file_path, "r", encoding="utf-8") as file:
            conversation_text = file.read()

        # Pass the filename and text content to the result page
        return render_template('result.html', filename=filename, conversation=conversation_text, host_name=host_name, guest_name=guest_name, news_type=news_type)
    
    return render_template('generate.html', languages=supported_languages)


# Convert text to audio and play page route
@app.route('/audio', methods=['POST'])
def audio_page():
    filename = request.form.get('filename', '').strip()
    file_path = os.path.join(TEXT_DIR, filename)

    # Ensure the text file exists
    if not os.path.exists(file_path):
        return "Error: Conversation text not found.", 404

    # Read the conversation text from the file
    with open(file_path, "r", encoding="utf-8") as file:
        conversation = file.read()

    # Extract names from the filename
    name_parts = filename.replace(".txt", "").split("_")
    host_name, guest_name, news_type = name_parts[0], name_parts[1], "_".join(name_parts[2:])

    # Generate and store the audio file inside static/podcast/audio/
    audio_filename = filename.replace(".txt", ".mp3")
    audio_path = os.path.join(AUDIO_DIR, audio_filename)

    # Convert text to audio and save
    text_to_audio(conversation, host_name, guest_name, audio_path)

    return render_template('audio.html', audio_path=audio_filename)


# Function to check if a port is in use
def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("localhost", port)) == 0

# Function to find an open port only if needed
def find_free_port():
    if not is_port_in_use(5000):  # Try port 5000 first
        return 5000
    if not is_port_in_use(5050):  # Try port 5050 if 5000 is in use
        return 5050
    # If both are taken, find an available port dynamically
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("localhost", 0))
        _, port = sock.getsockname()
        return port

if __name__ == "__main__":
    port = int(os.environ.get("PORT", find_free_port()))  # Use default if available
    print(f"Starting Flask app on port {port}...")
    app.run(host="0.0.0.0", port=port, debug=True)

