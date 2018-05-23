from pybpodapi.com.arcom import ArCOM, ArduinoTypes
from pybpodapi.bpod_modules.bpod_module import BpodModule
import struct
import numpy as np
import wave

class AnalogOutputModule(object):
    
    COM_HANDSHAKE                   = 227
    COM_PLAY_WAVEFORM               = ord('P')
    COM_STOP_PLAYBACK               = ord('X')
    COM_LOAD_WAVEFORM               = ord('L')
    COM_SET_OUTPUT_RANGE            = ord('R')
    COM_SET_SAMPLING_PERIOD         = ord('S')
    COM_SET_LOOP                    = ord('O')
    COM_SET_STATE_MACHINE_REPORTING = ord('V')
    COM_SET_TRIGGER                 = ord('T')
    COM_LOAD_TRIGGER_PROFILE        = ord('F')
    COM_GET_PARAMETERS              = ord('N')
    COM_TRIGGER_STANDARD            = 0
    COM_TRIGGER_PROFILE             = 1

    def __init__(self, serialport = None):
        self._state = {}
        if serialport:
            self.open(serialport)

    def open(self, serialport):
        try:
            self.arcom = ArCOM().open(serialport,115200)
            self.arcom.write_array([self.COM_HANDSHAKE])
            ack = self.arcom.read_uint8()
            print('ack',ack)
            fwversion = self.arcom.read_uint32()
            print('fw version',fwversion)
            #self.get_parameters()
            #self.set_trigger_mode()
            #raise Exception('Could not connect to Analog Output Module')
        except:
            return False
        return True

    def disconnect(self):
        print('disconnecting')
        if hasattr(self,'arcom'):
            self.arcom.close()

    def send(self, value):
        self.arcom.write_array([value])

    def play(self,channels,wave):
        self.send(self.COM_PLAY_WAVEFORM)
        self.send(channels)
        self.send(wave)


    def stop(self):
        self.send(self.COM_STOP_PLAYBACK)


    def _load_waveform(self, filename, channel):
        print('loading waveform',filename,'into channel',channel)
        wf = wave.open(filename,'r')
        print(
            wf.getparams()
        )
        nch = wf.getnchannels()

        nsamples = wf.getnframes()*nch
        
        framerate = wf.getframerate()*nch

        f = open(filename,'rb')
        # send everything through the com port
        self.send(self.COM_LOAD_WAVEFORM)
        self.send(int(channel))
        
        self.arcom.write_array(nsamples.to_bytes(4,'little'))
        
        #rawb = wf.readframes(100)
        i = 0
        print('first byte read')
        while True:
            #print('pre write',rawb)
            rawb = wf.readframes(4000)
            if not rawb:
                print('breaking')
                break
            self.arcom.write_array(rawb)
            #print('byte sent')
            i = i+len(rawb)
            print('read',len(rawb),'of',nsamples*nch,'total read:',i)
            #print(wf.getparams())
            
        print('ended loop')

        #expect ack
        ack = self.arcom.read_uint8()
        print('ack',ack)

        return framerate


    def set_output_range(self, value):
        self.send(self.COM_SET_OUTPUT_RANGE)
        self.send(value)
        ack = self.arcom.read_uint8()
        print('ack',ack)


    def set_sampling_period(self, value):
        #if value < 1 or value > 200000:
            #return False
        samplinPeriodMicroseconds = (1/value)*1000000
        print('setting sample time to',samplinPeriodMicroseconds)
        self.send(self.COM_SET_SAMPLING_PERIOD)
        #check if values are in decent values
        self.arcom.write_array(struct.pack('f',samplinPeriodMicroseconds))
        return True
        #ack = self.arcom.read_uint8()
        #print('ack',ack)


    def set_loop(self,loopmodes,loopdurations):
        self.send(self.COM_SET_LOOP)
        self.arcom.write_array(loopmodes)
        #self.arcom.write_array(loopdurations)
        for a in loopdurations:
            print(a.to_bytes(4,'little'))
            self.arcom.write_array(a.to_bytes(4,'little'))
        ack = self.arcom.read_uint8()
        print('ack',ack)



    def set_state_machine_reporting(self, values):
        print('setting state machine reporting',values)
        self.send(self.COM_SET_STATE_MACHINE_REPORTING)
        for a in values:
            self.send(a)
        ack = self.arcom.read_uint8()
        print('ack',ack)
        


    def set_trigger_mode(self, value):
        self.send(self.COM_SET_TRIGGER)
        self.send(value)
        ack = self.arcom.read_uint8()
        print(ack)
        

    def load_trigger_profile(self):
        pass


    def get_parameters(self):
        self.send(self.COM_GET_PARAMETERS)
        self._state = {}
        self._state['nChannels'] = self.arcom.read_uint8()
        self._state['maxWaves'] = self.arcom.read_uint16()
        self._state['triggerMode'] = self.arcom.read_uint8()
        self._state['triggerProfileEnable'] = self.arcom.read_uint8()
        self._state['maxTriggerProfiles'] = self.arcom.read_uint8()
        self._state['rangeIndex'] = self.arcom.read_uint8()
        self._state['timerPeriod'] = round((1/self.arcom.read_float32())*1000000)
        self._state['sendBpodEvents'] = self.arcom.read_uint8_array(self._state['nChannels'])
        self._state['loopMode'] = self.arcom.read_uint8_array(self._state['nChannels'])
        self._state['loopDuration'] = self.arcom.read_uint32_array(self._state['nChannels'])
        print(self._state)
        return self._state
        
        