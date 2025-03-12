from flask import Flask, render_template, request, redirect, url_for
import openai
import requests
from google.cloud import texttospeech, secretmanager, storage
from pydub import AudioSegment
import gender_guesser.detector as gender
import os
import json
from dotenv import load_dotenv
import tempfile
import datetime

# Load environment variables from .env if running locally
load_dotenv()

app = Flask(__name__)

# Load API keys from environment variables
openai.api_key = os.getenv('OPENAI_API_KEY')
serp_api_key = os.getenv('SERP_API_KEY')

# Initialize Secret Manager Client
secret_client = secretmanager.SecretManagerServiceClient()

def get_tts_credentials():
    environment = os.getenv('ENVIRONMENT', 'production')
    if environment == 'local':
        # Use local credentials path if running locally
        google_application_credentials = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = google_application_credentials
        print(f"Using local credentials at: {google_application_credentials}")
    else:
        # Retrieve the JSON credentials from Secret Manager
        name = f"projects/<project_id>/TTS_CREDENTIALS/versions/latest"
        response = secret_client.access_secret_version(name=name)
        credentials_data = response.payload.data.decode("UTF-8")
        
        # Create a temporary file to store credentials in production
        temp_credentials_path = "/tmp/tts_credentials.json"
        with open(temp_credentials_path, "w") as f:
            f.write(credentials_data)
        
        # Set the GOOGLE_APPLICATION_CREDENTIALS path
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = temp_credentials_path
        print(f"Using credentials from Secret Manager")

# **Call get_tts_credentials to initialize the credentials**
get_tts_credentials()

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
        # Log an error if news fetch fails
        print(f"Error fetching news: {response.status_code}")
        return []

# Function to generate podcast conversation
def generate_conversation(guest_name, host_name, news_titles, news_type):
    if not news_titles:
        return "Sorry, no news available at the moment."

    # Conversation prompt
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
    The tone, emotion, and flow should adapt naturally based on the genre, ensuring a dynamic, human-like exchange in English.
    """

    # Call OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": f"You are an AI podcast host named {host_name}."},
            {"role": "user", "content": conversation_prompt}
        ]
    )

    # Extract and format the generated conversation text
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

def upload_to_bucket(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the Google Cloud Storage bucket, creating a unique filename if necessary."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    
    # Generate a unique name if the file already exists
    blob = bucket.blob(destination_blob_name)
    if blob.exists():
        base_name, extension = os.path.splitext(destination_blob_name)
        counter = 1
        while blob.exists():
            destination_blob_name = f"{base_name}_{counter}{extension}"
            blob = bucket.blob(destination_blob_name)
            counter += 1

    # Upload the file
    blob.upload_from_filename(source_file_name)
    print(f"File {source_file_name} uploaded to {destination_blob_name}.")

    # Return the URL of the uploaded file
    return f"https://storage.googleapis.com/{bucket_name}/{destination_blob_name}"

def text_to_audio(conversation, host_name, guest_name):
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
    silence = AudioSegment.silent(duration=500)  # 500 ms silence

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

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio_file:
            temp_audio_file.write(response.audio_content)
            audio_clips.append(AudioSegment.from_mp3(temp_audio_file.name) + silence)
            os.remove(temp_audio_file.name)

    combined_audio = sum(audio_clips) if audio_clips else AudioSegment.silent(duration=1000)
    
    # Save the combined audio to a temporary file
    combined_audio_path = "/tmp/combined_conversation.mp3"
    combined_audio.export(combined_audio_path, format="mp3")

    # Define the bucket and path for the file
    bucket_name = "singular-glow-279213.appspot.com"  # Your bucket name
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")  # Add timestamp for uniqueness
    base_filename = f"audio/conversation_{host_name}_{guest_name}_{timestamp}.mp3"

    # Upload to Cloud Storage and get the URL
    audio_url = upload_to_bucket(bucket_name, combined_audio_path, base_filename)
    
    return audio_url

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
        news_type = request.form.get('news_type', '').strip()
        
        news_titles = fetch_google_news(news_type)
        generated_conversation = generate_conversation(guest_name, host_name, news_titles, news_type)
        
        return render_template('result.html', conversation=generated_conversation, host_name=host_name, guest_name=guest_name)
    
    return render_template('generate.html', languages=supported_languages)

# Convert text to audio and play page route
@app.route('/audio', methods=['POST'])
def audio_page():
    conversation = request.form.get('conversation', '')
    host_name = request.form.get('host_name', '')
    guest_name = request.form.get('guest_name', '')
    
    # Generate audio and get the Cloud Storage URL
    audio_url = text_to_audio(conversation, host_name, guest_name)
    
    return render_template('audio.html', audio_url=audio_url)


if __name__ == '__main__':
    app.run(debug=True)
