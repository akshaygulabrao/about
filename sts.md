[Home](./index.html)

Akshay Gulabrao 11 July 2025

# Leveraging Speech-to-Text Models for Financial Insights  
Experts in their field routinely publish podcasts on YouTube. Speech-to-Text models may prove to be a useful tool to efficiently bring their insights to the stock market. In this paper, I introduce a pipeline that can be used to bring financial insights to the stock market in an efficient manner, using Martin Shkreli, a biotech expert as an example.

---

## Leveraging YouTube for Financial Insights  
I’m currently using **yt-dlp**, **Whisper**, and **text-embedding-3-small** to listen to everything Martin Shkreli says. The 3-small embeddings go into a **SQLite3** database that I query before feeding the text to an LLM.

- **yt-dlp**  
- **Whisper**  
- **text-embedding-3-small**  
- **llm CLI tool** (by Simon Willison)  
- **Runpod.io**  

---

## Components

### yt-dlp  
[yt-dlp](https://github.com/yt-dlp/yt-dlp) downloads YouTube videos by simulating a browser with all relevant cookies, rotating proxies to avoid IP bans, and making the exact same API calls that would be used to watch a YouTube video online.  
⚠️ This may not be a stable solution for very long; YouTube could start requiring a proof-of-origin tag.

### Whisper  
OpenAI’s open-source speech-to-text model. I use it to convert the raw audio from each YouTube video into a `.vtt` transcript.  
Future work: I may switch to a hosted API to reduce operational overhead.

### Runpod.io  
Currently used for two things:  
1. Downloading the video.  
2. Running Whisper.  

I don’t think this is a good long-term choice; I want my research to focus on **building the dataset**, not on infrastructure innovation.

### text-embedding-3-small  
OpenAI’s official embedding model. This is my biggest cost driver—roughly **$0.01 per day** at current volume. I should migrate away from it as soon as possible.

### llm CLI tool  
A command-line tool created by [Simon Willison](https://github.com/simonw/llm). Excellent documentation and dead-simple to use.

---

## Data  
My main contribution should be **the dataset itself** and **Whisper fine-tuning methods**. Avoiding a transcript API might still be worthwhile to maintain full control over the pipeline.