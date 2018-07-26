# generate wav file containing sine waves
# FB36 - 20120617
import math, wave, array, struct, numpy as np
from pybpod_analogoutput_module.module_api import AnalogOutputModule

amplitude   = 1.0
duration    = 3 # seconds
freq        = 1000 # of cycles per second (Hz) (frequency of the sine waves)
volume      = 100 # percent
sampleRate  = 96000 # of samples per second (standard)
numChan     = 1 # of channels (1: mono, 2: stereo)
dataSize    = 2 # 2 bytes because of using signed short integers => bit depth = 16


samples = np.arange(0, duration, 1/sampleRate)
wave    = amplitude * np.sin(2*math.pi*freq*samples)


"""
data = array.array('h') # signed short integer (-32768 to 32767) data
numSamplesPerCyc = int(sampleRate / freq)
numSamples = sampleRate * duration
for i in range(numSamples):
    
    sample = 32767 * float(volume) / 100
    sample *= math.sin(math.pi * 2 * (i % numSamplesPerCyc) / numSamplesPerCyc)
    data.append(int(sample))
"""

m = AnalogOutputModule('/dev/ttyACM0')

print(m.set_sampling_period(sampleRate))

print(m.load_waveform(wave, 1))

print(m.play(1, 1))