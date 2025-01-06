# AI Amplified

AI Amplified is a dynamic web application that revolutionizes podcast creation using AI technology. In its first phase, the project generates human-like conversations between a host and a guest based on the latest BBC news, using OpenAI’s GPT-4 language model. The ultimate aim of this project is to streamline the content creation process by automatically generating podcast conversations from news topics and presenting them in a structured and engaging format.

## Project Overview

### Features:
- Fetches the latest news from the BBC API, allowing users to select the type of news they want to discuss.
- Users can input the guest's name, host's name, and the language for the conversation.
- AI generates a podcast-like conversation based on the selected news topics.
- Conversations are structured in a human-like dialogue between the host and guest.
  
### Future Phases:
- **Phase 2**: Convert the generated conversation into an audio format, utilizing text-to-speech technology.
- **Future Scope**: The project could eventually evolve into generating fully animated videos where AI-generated avatars of the host and guest interact as if they are in a real podcast.

## Technical Portfolio

### Core Technologies:
- **Flask**: Flask is used as the web framework to manage the frontend and backend, enabling user interaction and API calls.
- **OpenAI GPT-4**: GPT-4 is leveraged to generate coherent and dynamic conversations based on news topics.
- **BBC News API**: The BBC API is used to fetch the latest news headlines and topics based on user preferences.
- **HTML/CSS**: Frontend designed using HTML5 and custom CSS for styling the landing, generation, and result pages.

## How to Clone and Run This Project

### Prerequisites:
- Python 3.x
- A virtual environment (optional but recommended)
- API Key for OpenAI (you can generate it from [OpenAI's website](https://beta.openai.com/signup/))

### Steps:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/ai_amplified.git
    cd ai_amplified
    ```

2. **Create a virtual environment** (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use venv\Scripts\activate
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up OpenAI API Key**:
    - In the `app.py` file, replace `'your-openai-api-key'` with your actual OpenAI API key.

5. **Run the Flask application**:
    ```bash
    python app.py
    ```

6. **Access the web app**:
    - Open your browser and navigate to `http://127.0.0.1:5000/` to use the application.

## Evaluation Metrics

Here are a few ways to evaluate this project:

1. **Coherence of Conversations**: How well do the generated conversations flow between the host and guest? The conversation should be natural and contextually relevant based on the news topic.
   
2. **Relevance to the News**: Measure how accurately the generated conversation reflects the news headlines or topics that are fetched from the BBC API. This can be manually assessed by comparing the conversation with the real news.

3. **User Experience**: How intuitive and seamless is the interaction for users? This includes ease of input (guest name, host name, language), fast response times, and clear presentation of the conversation.

## Phase 2 and Future Scope

- In **Phase 2**, the focus will be on converting the generated text into high-quality audio using text-to-speech technologies.
- The **future scope** of this project may include AI-generated video avatars that interact with each other, mimicking a real conversation between professional podcast hosts and guests.


Thank you for exploring AI Amplified! We look forward to expanding this project and making the podcast creation process more streamlined and engaging.




# AI Amplified

AI Amplified is a dynamic web application that revolutionizes podcast creation using AI technology. In its first phase, the project generates human-like conversations between a host and a guest based on the latest BBC news, using OpenAI’s GPT-4 language model. The ultimate aim of this project is to streamline the content creation process by automatically generating podcast conversations from news topics and presenting them in a structured and engaging format.

## Project Overview

### Features:
- Fetches the latest news from the BBC API, allowing users to select the type of news they want to discuss.
- Users can input the guest's name, host's name, and the language for the conversation.
- AI generates a podcast-like conversation based on the selected news topics.
- Conversations are structured in a human-like dialogue between the host and guest.
  
### Future Phases:
- **Phase 2**: Convert the generated conversation into an audio format, utilizing text-to-speech technology.
- **Future Scope**: The project could eventually evolve into generating fully animated videos where AI-generated avatars of the host and guest interact as if they are in a real podcast.

## Technical Portfolio

### Core Technologies:
- **Flask**: Flask is used as the web framework to manage the frontend and backend, enabling user interaction and API calls.
- **OpenAI GPT-4**: GPT-4 is leveraged to generate coherent and dynamic conversations based on news topics.
- **BBC News API**: The BBC API is used to fetch the latest news headlines and topics based on user preferences.
- **HTML/CSS**: Frontend designed using HTML5 and custom CSS for styling the landing, generation, and result pages.

## How to Clone and Run This Project

### Prerequisites:
- Python 3.x
- A virtual environment (optional but recommended)
- API Key for OpenAI (you can generate it from [OpenAI's website](https://beta.openai.com/signup/))

### Steps:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/ai_amplified.git
    cd ai_amplified
    ```

2. **Create a virtual environment** (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use venv\Scripts\activate
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up OpenAI API Key**:
    - In the `app.py` file, replace `'your-openai-api-key'` with your actual OpenAI API key.

5. **Run the Flask application**:
    ```bash
    python app.py
    ```

6. **Access the web app**:
    - Open your browser and navigate to `http://127.0.0.1:5000/` to use the application.

## Evaluation Metrics

Here are a few ways to evaluate this project:

1. **Coherence of Conversations**: How well do the generated conversations flow between the host and guest? The conversation should be natural and contextually relevant based on the news topic.
   
2. **Relevance to the News**: Measure how accurately the generated conversation reflects the news headlines or topics that are fetched from the BBC API. This can be manually assessed by comparing the conversation with the real news.

3. **User Experience**: How intuitive and seamless is the interaction for users? This includes ease of input (guest name, host name, language), fast response times, and clear presentation of the conversation.

## Phase 2 and Future Scope

- In **Phase 2**, the focus will be on converting the generated text into high-quality audio using text-to-speech technologies.
- The **future scope** of this project may include AI-generated video avatars that interact with each other, mimicking a real conversation between professional podcast hosts and guests.

Thank you for exploring AI Amplified! We look forward to expanding this project and making the podcast creation process more streamlined and engaging.

---

## Phase 2: Audio-Enhanced Podcast Automation

In **Phase 2**, we have expanded AI Amplified’s capabilities by adding **text-to-speech** functionality, enabling the generated conversations to be converted into high-quality audio files. This phase marks a significant enhancement as the application now produces audio-ready content, bringing us closer to full podcast automation.

### What is AI Amplified?
This application can be considered an **LLM Agent** focused on content generation for podcasts. It acts as an "AI podcaster" capable of:
1. Fetching real-time news topics.
2. Generating a coherent conversation between predefined characters.
3. Converting the conversation to audio, making it ready for distribution.

The AI operates autonomously by interacting with APIs, fetching data, generating conversations, and producing audio—mimicking the roles of a podcast writer, host, and editor.

### Technologies and Changes in Phase 2

Compared to Phase 1, we introduced new technologies and features:
- **Google Cloud Text-to-Speech (TTS)**: Converts text conversations into audio format, bringing the AI-generated dialogue to life.
- **Google Cloud Storage**: Stores generated audio files, ensuring scalability and access through unique URLs.
- **Google Secret Manager**: Securely manages API keys and credentials, particularly for production deployments.
- **Temporary Storage Handling**: Utilizes `/tmp` for temporary storage, optimizing storage management in cloud environments.

### Tasks Accomplished in Phase 2
- Implemented text-to-speech functionality for dynamic, voice-activated podcasts.
- Enhanced security by integrating Secret Manager for managing credentials in production.
- Enabled scalable storage for audio files using Google Cloud Storage.
- Designed a unique naming convention for audio files to handle multiple generations without overwriting.

---

## Application APIs and Workflow

### Workflow
1. **Fetch News API**: Uses BBC’s SerpAPI to fetch the latest news headlines.
2. **Conversation Generation API**: OpenAI’s GPT-4 generates conversation based on fetched news topics.
3. **Text-to-Speech Conversion API**: Google Cloud TTS converts text to audio.
4. **Storage and Access API**: Google Cloud Storage hosts the audio file, generating a shareable URL.

### Architecture Diagram

```plaintext
          +---------------------+
          |    User Request     |
          +----------+----------+
                     |
                     v
          +----------+----------+
          |  Fetch News API     |
          |    (SerpAPI)        |
          +----------+----------+
                     |
                     v
          +----------+----------+
          | Conversation API    |
          |  (OpenAI GPT-4)     |
          +----------+----------+
                     |
                     v
          +----------+----------+
          | Text-to-Speech API  |
          |   (Google TTS)      |
          +----------+----------+
                     |
                     v
          +----------+----------+
          |  Cloud Storage      |
          |  (Google Cloud)     |
          +----------+----------+
                     |
                     v
          +----------+----------+
          |     Web App         |
          |    (Flask + HTML)   |
          +---------------------+

```

## How to Clone and Run This Project

### Prerequisites:
- Python 3.x
- A virtual environment (optional but recommended)
- API keys for OpenAI, SerpAPI, and Google Cloud (Text-to-Speech, Storage, and Secret Manager)

### Local Setup

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/ai_amplified.git
    cd ai_amplified
    ```

2. **Create a virtual environment** (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use venv\Scripts\activate
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables**:
   - Add your OpenAI, SerpAPI, and Google Cloud credentials to a `.env` file or Google Secret Manager.
   - Example `.env`:
     ```bash
     OPENAI_API_KEY=your_openai_api_key
     SERP_API_KEY=your_serp_api_key
     GOOGLE_APPLICATION_CREDENTIALS=/path/to/google_credentials.json
     ```

5. **Run the Flask application**:
    ```bash
    python app.py
    ```

6. **Access the web app**:
    - Open your browser and navigate to `http://127.0.0.1:5000/`.

---

## Deploying on Google Cloud Platform (GCP)

1. **Enable Required Services**:
   - Enable Cloud Run, Cloud Storage, and Secret Manager in your GCP project.

2. **Upload Credentials to Secret Manager**:
   - In GCP Console, go to Secret Manager, create a new secret (e.g., `TTS_CREDENTIALS`), and upload your Google Cloud credentials JSON file.

3. **Set Up Environment Variables**:
   - In `app.yaml`, define environment variables for OpenAI, SerpAPI, and Secret Manager locations.

4. **Deploy to App Engine**:
    ```bash
    gcloud app deploy app.yaml
    ```

5. **Access the Deployed Application**:
   - After deployment, your app’s URL is available in the App Engine dashboard.

---

## Future Scope

Looking forward, the application has the potential for further advancements:

- **AI-Generated Animated Avatars**: Convert the audio into a visual format, where avatars of the host and guest speak the conversation.
- **Voice Customization**: Mimic specific artists or public figures based on their vocal profiles, creating personalized audio experiences.

Thank you for exploring AI Amplified! We are excited to continue evolving this project to make content creation simpler and more engaging.


