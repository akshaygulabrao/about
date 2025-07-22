[Home](./index.html)

Akshay Gulabrao 11 July 2025

# Domain Specific Speech Recognition

Speech recognition helps aggregate large amounts of audio into actionable insight. One of the problems with speech recognition is that words are highly contextual. In highly technical domains, models still tend to misinterpret the meaning of words for their far more commonplace counterparts. Here I investigate the quality of transcription of Martin Shkreli's pharmaceutical/financial youtube videos with respect to different API providers and use OpenAI's whisper as a control.

## The test

I have uploaded an audio file of martin shkreli's stream to [gd](). I used the following openai whisper command:
```bash
whisper audio.wav --model medium --language en --word_timestamps True -f vtt
```