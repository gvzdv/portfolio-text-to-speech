# brew install poppler

import pdftotext
import os
from google.cloud import texttospeech

# Set up authentication environment variable
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "daring-harmony-379101-6a518e6f8c41.json"


# Get the path to the file from the user
path = input("Enter the path to the .pdf file:\n")
filename, ext = os.path.splitext(path)


def synthesize_text(text):

    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Build the voice request, select the language code ("en-US") and the ssml voice gender ("female")
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Wavenet-F",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    )

    # Select the type of audio file returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary
    with open(f"{filename}.mp3", "wb") as out:

        # Write the response to the output file.
        out.write(response.audio_content)
        print('Audio content written to the original file directory')


# Open the PDF file in read-binary mode
with open(path, 'rb') as file:

    # Create a pdftotext PDF object
    pdf = pdftotext.PDF(file)
    text_to_read = ""

    # Loop through each page in the PDF file
    for page in pdf:

        # Convert all pages into text
        text_to_read += page

    # Convert text to speech
    synthesize_text(text_to_read)

