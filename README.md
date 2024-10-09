# VOICE-TO-VOICE-AI-TRANSLATION
A voice-to-voice translator is a technology that enables real-time translation of spoken language from one language to another. It typically uses automatic speech recognition (ASR) to convert spoken words into text, followed by machine translation (MT) to translate the text into the target language.

# Voice-to-Voice Translator

A real-time voice-to-voice translation application that transcribes audio input, translates the text into multiple languages, and converts the translated text back into audio. This project utilizes several APIs including AssemblyAI for audio transcription, a translation library for text translation, and ElevenLabs for text-to-speech conversion.

## Features

- **Real-time Audio Transcription**: Converts spoken language from audio files into text.
- **Multi-language Translation**: Translates the transcribed text into Telugu, Japanese, and Arabic.
- **Text-to-Speech Conversion**: Converts the translated text back into audio format in the respective languages.
- **User-friendly Interface**: Built using Gradio for easy interaction.

## Requirements

- Python 3.x
- Required libraries:
  - `gradio`
  - `assemblyai`
  - `translate`
  - `elevenlabs`
  
You can install the required libraries using pip:

```bash
pip install gradio assemblyai translate elevenlabs
