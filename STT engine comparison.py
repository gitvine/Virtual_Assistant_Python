from ibm_watson import SpeechToTextV1
import json
import speech_recognition as sp

#For IBM we need to authenticate separately
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
authenticator = IAMAuthenticator('xxxxxxxxxx')
speech_to_text = SpeechToTextV1(
    authenticator=authenticator
)
#Setting service URL for IBM watson
speech_to_text.set_service_url('https://api.eu-gb.speech-to-text.watson.cloud.ibm.com/instances/ea66102e-5ad2-4c42-9910-xxxxxxx')
#creating an instance of a speech recognition class
rec = sp.Recognizer()


def decode_sphinx(audio):
    #Function to carry out speech to text conversion with Sphinx
    try:
        detected=rec.recognize_sphinx(audio)
        print("According to Sphinx you said " + detected)
        if(detected.strip().upper() == 'ASSISTANT'):
            return 1
        else:
            return 0
    except:
        print("An exception occurred")
        return 0

def decode_google(audio):
    #Function to carry out speech to text conversion with Google web speech
    try:
        detected=rec.recognize_google(audio)
        print("According to Google web speech you said " + detected)
        if(detected.strip().upper() == 'ASSISTANT'):
            return 1
        else:
            return 0
    except:
        print("An exception occurred")
        return 0


def decode_houndify(audio):
    # Function to carry out speech to text conversion with Houndify
    try:
        detected = rec.recognize_houndify(audio,'xxxxxxxxx==','xxxxxxxxxxxx')
        print("According to Houndify you said " + detected)
        if (detected.strip().upper() == 'ASSISTANT'):
            return 1
        else:
            return 0
    except:
        print("An exception occurred")
        return 0

def decode_ibm(audio):
    # Function to carry out speech to text conversion with IBM watson
    try:
        speech_recognition_results = speech_to_text.recognize(audio=audio.get_wav_data(),
                                                              content_type='audio/wav').get_result()
        json_object = json.loads(json.dumps(speech_recognition_results, indent=2))
        detected = json_object['results'][0]['alternatives'][0]['transcript']
        print("According to IBM Watson you said " + detected )
        if (detected.strip().upper() == 'ASSISTANT'):
            return 1
        else:
            return 0
    except:
        print("An exception occurred")
        return 0






#Initialising accuracy count for all 4 engines
sphinx_accuracy=0
google_accuracy =0
houndify_accuracy =0
ibm_accuracy =0


for i in range(1, 101):
    # obtaining audio from the files one after another through loop
    audio_file = sp.AudioFile('assistant'+str(i)+'.wav')
    with audio_file as source:
        #using all four models one after another to test audio file
        audio = rec.record(source)
        sphinx_accuracy += decode_sphinx(audio)
        google_accuracy += decode_google(audio)
        houndify_accuracy += decode_houndify(audio)
        ibm_accuracy += decode_ibm(audio)
print("Sphinx accuracy:",sphinx_accuracy,"Google accuracy:",google_accuracy,"Houndify accuracy:",houndify_accuracy,"IBM accuracy:",ibm_accuracy)
