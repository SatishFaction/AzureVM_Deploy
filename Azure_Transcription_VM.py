import azure.cognitiveservices.speech as speechsdk
import time
import datetime
import os
os.chdir(r'C:\Users\hp\Desktop\Azure Transcriptions\English_Audio_Wav')
def speech_to_text(f):
    
    # Creates an instance of a speech config with specified subscription key and service region.
    # Replace with your own subscription key and region identifier from here: https://aka.ms/speech/sdkregion
    speech_key, service_region = "2a9ce48acf3b4e31bd16ad0dadbe287b", "centralindia"
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

    # Creates an audio configuration that points to an audio file.
    # Replace with your own audio filename.
    audio_filename = f
    audio_input = speechsdk.audio.AudioConfig(filename=audio_filename)
    # Creates a recognizer with the given settings
    speech_config.speech_recognition_language="en-IN"
    #speech_config.request_word_level_timestamps()
    #speech_config.enable_dictation()
    speech_config.output_format = speechsdk.OutputFormat(1)

    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)

    #result = speech_recognizer.recognize_once()
    all_results = []



    #https://docs.microsoft.com/en-us/python/api/azure-cognitiveservices-speech/azure.cognitiveservices.speech.recognitionresult?view=azure-python
    def handle_final_result(evt):
        all_results.append(evt.result.text) 
    
    
    done = False

    def stop_cb(evt):
        print('CLOSING on {}'.format(evt))
        speech_recognizer.stop_continuous_recognition()
        nonlocal done
        done= True

    #Appends the recognized text to the all_results variable. 
    speech_recognizer.recognized.connect(handle_final_result) 

    #Connect callbacks to the events fired by the speech recognizer & displays the info/status
    #Ref:https://docs.microsoft.com/en-us/python/api/azure-cognitiveservices-speech/azure.cognitiveservices.speech.eventsignal?view=azure-python   
    speech_recognizer.recognizing.connect(lambda evt: print('RECOGNIZING: {}'.format(evt)))
    speech_recognizer.recognized.connect(lambda evt: print('RECOGNIZED: {}'.format(evt)))
    speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))
    # stop continuous recognition on either session stopped or canceled events
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    speech_recognizer.start_continuous_recognition()

    while not done:
        time.sleep(.5)
            
    #print("Printing all results:")
    #print(all_results)
    return all_results

#calling the conversion through a function
import pandas as pd
filenames = pd.read_csv(r"C:\\Users\\hp\\Desktop\\Azure Transcriptions\\names.csv")
df = pd.DataFrame(columns = ['Filename', 'Transcript'])

for f in os.listdir(r"C:\Users\hp\Desktop\Azure Transcriptions\English_Audio_Wav"):
    if f in filenames['Name'].tolist():
        result=speech_to_text(f)
        string=""
        for i in result:
            string=string+i
        df = df.append({'Filename': f, 'Transcript': string}, ignore_index = True)


df.to_excel("English_Audio_Files.xlsx")





