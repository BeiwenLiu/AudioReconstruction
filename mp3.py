# -*- coding: utf-8 -*-
"""
Created on Thu Sep 08 00:00:37 2016

@author: user
"""

import wave
import audioop
import os
from pydub import AudioSegment


def downsampleWav(src, dst, inrate=44100, outrate=22050, inchannels=1, outchannels=1):
    if not os.path.exists(src):
        print 'Source not found!'
        return False
    
    s_read = wave.open(src, 'r')
    s_write = wave.open(dst, 'w')
    

    n_frames = s_read.getnframes()
    data = s_read.readframes(n_frames)

    try:
        converted = audioop.ratecv(data, 2, inchannels, inrate, outrate, None)
        if outchannels == 1:
            converted = audioop.tomono(converted[0], 2, 1, 0)
    except:
        print 'Failed to downsample wav'
        return False

    try:
        s_write.setparams((outchannels, 2, outrate, 0, 'NONE', 'Uncompressed'))
        s_write.writeframes(converted)
    except:
        print 'Failed to write wav'
        return False

    try:
        s_read.close()
        s_write.close()
    except:
        print 'Failed to close wav files'
        return False

    return True
    
def downSampleMP3(src):
    s = AudioSegment.from_mp3("mp3/{}".format(src))
    tempSrc = str(src)[:-4]
    s.export("wav/{}.wav".format(tempSrc), format="wav")
    downsampleWav("wav/{}.wav".format(tempSrc),"wav/{}DS.wav".format(tempSrc))
    s1 = AudioSegment.from_wav("wav/{}DS.wav".format(tempSrc))
    s1.export("mp3/{}DS.mp3".format(tempSrc), format="mp3")
    return "{}DS.mp3".format(tempSrc)
    
def unitSelection(src, sliceSize):
    sample = AudioSegment.from_mp3("mp3/{}".format(src))
    tempSrc = str(src)[:-4]
    print sample.duration_seconds
    previousSlice = 0
    currentSlice = sliceSize
    counter = 0
    while currentSlice < sample.duration_seconds * 1000:
        sample[previousSlice:currentSlice].export("mp3/units/{}Unit{}.mp3".format(tempSrc, counter), format="mp3")
        previousSlice = currentSlice
        currentSlice += sliceSize
        counter += 1

def main(filename,downsample,sliceSize):
    if downsample == True:
        tempFile = downSampleMP3(filename)
        unitSelection(tempFile,sliceSize)
    else:
        unitSelection(filename,sliceSize)
    
#mp3 file must be in mp3/file before passing in filename
#False to indicate whether you want to downsample
#indicate sliceSize        
main("RainsDS.mp3",False,500)
    
    

    