from flask import Flask, render_template, request, redirect, url_for
import openai
import requests
from gtts import gTTS
from pydub import AudioSegment
import random
import os
import gender_guesser.detector as gender

app = Flask(__name__)

# OpenAI API Key
openai.api_key = 'your-openai-key'

# SerpApi Key
serp_api_key = 'your-serp-api-key'


# Supported languages (limited to English for now)
supported_languages = {
    "English": "english"
}

# Initialize the gender detector
detector = gender.Detector()

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

    conversation_prompt = f"""
    Create a 10-minute {news_type} podcast conversation between {host_name} (the host) and {guest_name} (the guest).
    Discuss the following news headlines:
       - "{news_titles[0]}"
       - "{news_titles[1]}"
       - "{news_titles[2]}"
       - "{news_titles[3]}"
       - "{news_titles[4]}"
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

# Function to assign voices based on detected gender
def assign_voice_by_gender(name):
    gender_result = detector.get_gender(name.split()[0])
    if gender_result in ["male", "mostly_male"]:
        return 'com'  # US male voice for male names
    elif gender_result in ["female", "mostly_female"]:
        return 'co.uk'  # UK female voice for female names
    else:
        return 'com'  # Default to US English for unknown gender

def text_to_audio(conversation, host_name, guest_name):
    # Determine voices for host and guest based on gender
    host_voice = assign_voice_by_gender(host_name)
    guest_voice = assign_voice_by_gender(guest_name)

    # Split conversation into lines and set up pauses
    lines = conversation.split('\n')
    audio_clips = []
    silence = AudioSegment.silent(duration=500)  # 500 ms silence between exchanges

    # Process each line and alternate voices
    for line in lines:
        if line.strip().startswith(host_name):
            text = line.replace(f"{host_name}: ", "")
            tts = gTTS(text=text, lang='en', tld=host_voice)
        elif line.strip().startswith(guest_name):
            text = line.replace(f"{guest_name}: ", "")
            tts = gTTS(text=text, lang='en', tld=guest_voice)
        else:
            continue  # Skip any unrecognized line

        # Save line audio temporarily, load into pydub, and append with pause
        temp_audio_path = "temp_audio.mp3"
        tts.save(temp_audio_path)
        audio_clip = AudioSegment.from_mp3(temp_audio_path)
        audio_clips.append(audio_clip + silence)

    # Combine all audio clips into one
    if audio_clips:
        combined_audio = audio_clips[0]
        for clip in audio_clips[1:]:
            combined_audio += clip
    else:
        # Handle case where no audio was generated
        combined_audio = AudioSegment.silent(duration=1000)  # 1 second of silence as a fallback

    final_audio_path = "static/combined_conversation.mp3"
    combined_audio.export(final_audio_path, format="mp3")

    # Clean up temporary audio file
    if os.path.exists(temp_audio_path):
        os.remove(temp_audio_path)

    return final_audio_path

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
@app.route('/audio')
def audio_page():
    conversation = request.args.get('conversation', '')
    host_name = request.args.get('host_name', '')
    guest_name = request.args.get('guest_name', '')
    
    audio_path = text_to_audio(conversation, host_name, guest_name)
    return render_template('audio.html', audio_path=audio_path)

if __name__ == '__main__':
    app.run(debug=True)