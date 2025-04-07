# -*- coding: utf-8 -*-
"""
Extended speaker playback script
================================
Script that runs a speaker playback file every X seconds to mimic a playback
experiment run over an hour or two. 

Required inputs
---------------
* A WAV file
* Have to check the sounddevice device number or full string which is there in the output of sounddevice.query_devices()
* An ASIO-based audio interface
* A microphone to record the playback

Generated outputs
-----------------
* Multiple WAV files (depending on how long the experiment is run)

Created on Mon Apr  7 08:41:54 2025

@author: theja
"""
import sounddevice as sd
import soundfile as sf
import os
import datetime as dt
import time 


def hhmmss_to_seconds(time_str):
    """Get seconds from time.
    Credit to: https://stackoverflow.com/a/6402859/4955732
    """
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)

def read_audiofile(filepath):
    audio, fs = sf.read(filepath)
    return audio, fs

def generate_ISOstyle_time_now():
    '''
    generates timestamp in yyyy-mm-ddTHH-MM-SS format
    
    based on  https://stackoverflow.com/a/28147286/4955732
    '''
    current_timestamp = dt.datetime.now().replace(microsecond=0).isoformat()
    current_timestamp = current_timestamp.replace(':', '-')
    current_timestamp = current_timestamp.replace('T', '_')
    return current_timestamp

if __name__ == "__main__":
    sd.default.device = 32 # or whatever the device string ID is when you check the output of 'sd.query_devices'
    
    print('hello')
    # how long to run the playbacks in HH:MM:SS
    duration = "00:01:00" 
    
    # gap between playbacks in seconds
    wait_time = 3 # seconds
    
    # path to the playback file
    pbkfile_path = 'playback_sweeps.wav'
    
    audio, fs = read_audiofile(pbkfile_path)
    
    try:
        nchannels = audio.shape[1]
    except:
        nchannels = 1 
        audio = audio.reshape(-1,1)
    
    start_time = time.time()    
    print('hi')
    # name by which sounddevice refers to the audio-interface by
    while time.time() <= start_time + hhmmss_to_seconds(duration):
        # Playback and record simultaneously
        
        
        print(audio.shape)
        rec_audio = sd.playrec(audio, channels=nchannels, samplerate=fs,
                                    blocking=True)
        
        # # save recording 
        current_filename = 'playback_recording'+generate_ISOstyle_time_now()+'.wav'
        sf.write(current_filename, rec_audio, fs)
        
        # wait a bit before starting the next play-rec
        time.sleep(wait_time)
        
        
    
    

