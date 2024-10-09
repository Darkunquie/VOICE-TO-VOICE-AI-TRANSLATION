import gradio as gr
import assemblyai as aai
from translate import Translator
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
import uuid
from pathlib import Path            



def voice_to_voice(audio_file):
    # Implement voice-to-voice translation logic here
    transcription_response = audio_translation(audio_file)
    if transcription_response.status == aai.TranscriptStatus.error:  # Changed from TranscriptionStatus to TranscriptStatus
        raise gr.Error(transcription_response.error)
    else:
        text = transcription_response.text
        #translation=text_translation(text)
        telugu_translation, jap_translation, arabic_translation = text_translation(text)
        audio_telugu_path = text_to_speech(telugu_translation)
        audio_jap_path = text_to_speech(jap_translation)
        audio_ar_path = text_to_speech(arabic_translation)

        telugu_path = Path(audio_telugu_path)
        jap_path = Path(audio_jap_path)
        arabic_path = Path(audio_ar_path) 

        return telugu_path, jap_path, arabic_path
def audio_translation(audio_file):
    # Implement audio translation logic here
    aai.settings.api_key="b5ed43a0a0d44559b944e4cdfa6f4156"
    transcriber=aai.Transcriber()
    transcription=transcriber.transcribe(audio_file)
    return transcription 
def text_translation(text):
    # Implement text translation logic here
    translator_te=Translator(from_lang="en",to_lang="te")
    telugu_text=translator_te.translate(text)
   # return telugu_translation
    translator_ja=Translator(from_lang="en",to_lang="ja")
    jap_text=translator_ja.translate(text)
    translator_ar=Translator(from_lang="en",to_lang="ar")
    arabic_text=translator_ar.translate(text)
    return telugu_text,jap_text,arabic_text
def text_to_speech(text):
    #ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
    client = ElevenLabs(
    api_key="sk_e2b3df4103680aaf3fc65005fe3bbcd216ae2b35f3e84ec3",
    )   
    response = client.text_to_speech.convert(
        voice_id="pNInz6obpgDQGcFmaJgB", # Adam pre-made voice
        optimize_streaming_latency=0,
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_multilingual_v2", # use the turbo model for low latency
        voice_settings=VoiceSettings(
            stability=0.5,
            similarity_boost=0.8,
            style=0.5 ,
            use_speaker_boost=True,
        ),
    )
    save_file_path = f"{uuid.uuid4()}.mp3"
    with open(save_file_path, "wb") as f:
        for chunk in response:
            if chunk:
                f.write(chunk)

    print(f"{save_file_path}: A new audio file was saved successfully!")

    # Return the path of the saved audio file
    return save_file_path
       
audio_input=gr.Audio(sources=["microphone","upload"],type="filepath")

demo = gr.Interface(
    fn=voice_to_voice,
    inputs=audio_input,
    outputs=[
       
        gr.Audio(label="Telugu"),

        gr.Audio(label="Japanese"),
        gr.Audio(label="Arabic")
    ],
    title="Audio Translator",
)

if __name__ == "__main__":
    demo.launch()