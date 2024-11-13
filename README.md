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
