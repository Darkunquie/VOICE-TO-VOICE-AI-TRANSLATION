import gradio as gr
import assemblyai as aai
from translate import Translator
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
import uuid
from pathlib import Path


def voice_to_voice(audio_file):
    transcription_response = audio_translation(audio_file)
    if transcription_response.status == aai.TranscriptStatus.error:
        raise gr.Error(transcription_response.error)
    else:
        text = transcription_response.text  # This is the transcribed text
        telugu_translation, jap_translation, arabic_translation = text_translation(text)
        audio_telugu_path = text_to_speech(telugu_translation)
        audio_jap_path = text_to_speech(jap_translation)
        audio_ar_path = text_to_speech(arabic_translation)

        telugu_path = Path(audio_telugu_path)
        jap_path = Path(audio_jap_path)
        arabic_path = Path(audio_ar_path)

        return str(telugu_path), str(jap_path), str(arabic_path), text, telugu_translation, jap_translation, arabic_translation  # Return all texts



def audio_translation(audio_file):
    aai.settings.api_key = "5246453409da48448048438cbb1b64df"
    transcriber = aai.Transcriber()
    transcription = transcriber.transcribe(audio_file)
    return transcription


def text_translation(text):
    translator_te = Translator(from_lang="en", to_lang="te")
    telugu_text = translator_te.translate(text)
    translator_ja = Translator(from_lang="en", to_lang="ja")
    jap_text = translator_ja.translate(text)
    translator_ar = Translator(from_lang="en", to_lang="ar")
    arabic_text = translator_ar.translate(text)
    return telugu_text, jap_text, arabic_text


def text_to_speech(text):
    client = ElevenLabs(
        api_key="sk_f6d7d41f0ddf51ccc17e95beeb0a93fef6ad8c21c7ee68b3"
    )
    response = client.text_to_speech.convert(
        voice_id="pNInz6obpgDQGcFmaJgB",
        optimize_streaming_latency=0,
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_multilingual_v2",
        voice_settings=VoiceSettings(
            stability=0.5,
            similarity_boost=0.8,
            style=0.5,
            use_speaker_boost=True,
        ),
    )
    save_file_path = f"{uuid.uuid4()}.mp3"
    with open(save_file_path, "wb") as f:
        for chunk in response:
            if chunk:
                f.write(chunk)

    print(f"{save_file_path}: A new audio file was saved successfully!")

    return save_file_path


audio_input = gr.Audio(sources=["microphone", "upload"], type="filepath")

# Update the Gradio interface to include text outputs for all languages
demo = gr.Interface(
    fn=voice_to_voice,
    inputs=audio_input,
    outputs=[
        gr.Audio(label="Telugu"),
        gr.Audio(label="Japanese"),
        gr.Audio(label="Arabic"),
        gr.Textbox(label="Transcribed Text (English)"),  # English text output
        gr.Textbox(label="Transcribed Text (Telugu)"),   # Telugu text output
        gr.Textbox(label="Transcribed Text (Japanese)"),  # Japanese text output
        gr.Textbox(label="Transcribed Text (Arabic)")      # Arabic text output
    ],
    title="Audio Translator",
)

if __name__ == "__main__":
    demo.launch()
