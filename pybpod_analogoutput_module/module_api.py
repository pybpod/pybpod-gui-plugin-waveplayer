from pybpodapi.com.arcom import ArCOM, ArduinoTypes
from pybpodapi.bpod_modules.bpod_module import BpodModule
import struct
import numpy as np
import wave

class AnalogOutputModule(object):
    
    COM_HANDSHAKE            = 227
    COM_PLAY_WAVEFORM        = ord('P')
    COM_STOP_PLAYBACK        = ord('X')
    COM_LOAD_WAVEFORM        = ord('L')
    COM_SET_OUTPUT_RANGE     = ord('R')
    COM_SET_SAMPLING_PERIOD  = ord('S')
    COM_SET_LOOP             = ord('O')
    COM_SET_BPOD_EVENTS      = ord('V')
    COM_SET_TRIGGER          = ord('T')
    COM_LOAD_TRIGGER_PROFILE = ord('F')
    COM_GET_PARAMETERS       = ord('N')
    
    CURRENT_FIRMWARE_VERSION = 1

    TRIGGER_MODE_NORMAL = 0
    TRIGGER_MODE_MASTER = 1
    TRIGGER_MODE_TOGGLE = 2

    RANGE_VOLTS = ['0V:5V', '0V:10V', '0V:12V', '-5V:5V', '-10V:10V', '-12V:12V']
    RANGE_VOLTS_0_5  = 0
    RANGE_VOLTS_0_10 = 1
    RANGE_VOLTS_0_12 = 2
    RANGE_VOLTS_MINUS5_5   = 3
    RANGE_VOLTS_MINUS10_10 = 4
    RANGE_VOLTS_MINUS12_12 = 5


    def __init__(self, serial_port = None):

        self.is_open = False

        if serial_port:
            self.open(serial_port)



    def open(self, serialport):

        self.arcom = ArCOM().open(serialport,115200)

        self.arcom.write_array([self.COM_HANDSHAKE])
        
        ack = self.arcom.read_uint8()

        if ack!=228:
            raise Exception('Could not connect =( ')
        
        version = self.arcom.read_uint32()
        if version < self.CURRENT_FIRMWARE_VERSION:
            raise Exception("""Error: old firmware detected - v{0}.
                The current version is: {1}.
                Please update the I2C messenger firmware using Arduino.""".format(
                version, self.CURRENT_FIRMWARE_VERSION
            ))
        self.firmware_version = version
        

        self.__get_parameters()
        self.__print_parameters()

        self.is_open = True


    def close(self):
        if hasattr(self,'arcom'):
            self.arcom.close()
            del self.arcom
        self.is_open = False

    def send(self, value):
        self.arcom.write_array([value])

    def play(self, channels, wave):
        self.send(self.COM_PLAY_WAVEFORM)
        self.send(channels)
        self.send(wave)


    def stop(self):
        self.send(self.COM_STOP_PLAYBACK)


    def load_waveform(self, wavform, channel):
        
        data2send  = ArduinoTypes.get_uint8_array([self.COM_LOAD_WAVEFORM, channel])
        data2send += ArduinoTypes.get_uint32_array([len(wavform)])

        wavform = np.array(wavform, dtype=np.int16)

        if self.output_range==0:
            positive_only = 1;
            voltage_width = 5;
        elif self.output_range==1:
            positive_only = 1;
            voltage_width = 10;
        elif self.output_range==2:
            positive_only = 1;
            voltage_width = 12;
        elif self.output_range==3:
            positive_only = 0
            voltage_width = 10
        elif self.output_range==4:
            positive_only = 0
            voltage_width = 20
        elif self.output_range==5:
            positive_only = 0
            voltage_width = 24        
        else:
            positive_only = 0
            voltage_width = 10
        
        min_wave = min(wavform);
        max_wave = max(wavform);
        max_range = voltage_width+(positive_only*0.5);
        min_range = ( (voltage_width/2) * -1 ) * ( 1 - positive_only )

        print(min_wave, max_wave, max_range, min_range)
        if (min_wave < min_range) or (max_wave > max_range):
            raise Exception('Error setting waveform: All voltages must be within the current range: TODO.')
        
        offset = (voltage_width/2)*(1-positive_only);
        wavbits = np.ceil(((wavform+offset)/voltage_width)*(2^(16)-1));

        data2send += ArduinoTypes.get_uint16_array(wavbits)

        self.arcom.write_array(data2send)
        
        #expect ack
        ack = self.arcom.read_uint8()
        print('ack',ack)

        return ack==1


    def set_output_range(self, value):
        self.arcom.write_array(ArduinoTypes.get_uint8_array( [self.COM_SET_OUTPUT_RANGE, value] ))
        ack = self.arcom.read_uint8()
        return ack==1

    def set_sampling_period(self, value):

        if value < 1 or value > 200000:
            raise Exception('Error setting sampling rate: valid rates are in range: [1;200000] Hz')
            
        sampling_period_microseconds = (1.0/value)*1000000.0

        self.send(self.COM_SET_SAMPLING_PERIOD)
        self.arcom.write_array(struct.pack('f',sampling_period_microseconds))
        ack = self.arcom.read_uint8()

        return ack==1


    def set_loop(self, loopmodes, loopdurations):

        if len(loopmodes)!=self.n_channels:
            raise Exception('Wrong loop modes')

        if len(loopdurations)!=self.n_channels:
            raise Exception('Wrong loop durations')

        bytes2send = ArduinoTypes.get_uint8_array(
            [self.COM_SET_LOOP] + values + self.loopdurations*self.sampling_rate
        )
        self.arcom.write_array(bytes2send)

        return self.arcom.read_uint8()==1


    def set_bpod_events(self, values):
        bytes2send = ArduinoTypes.get_uint8_array(
            [self.COM_SET_STATE_MACHINE_REPORTING] + values
        )
        self.arcom.write_array(bytes2send)
        ack = self.arcom.read_uint8()

        if ack==1:
            self._trigger_profiles = trigger_profiles
        return ack==1
        
    def set_trigger_mode(self, value):
        self.arcom.write_array(
            ArduinoTypes.get_uint8_array([self.COM_SET_TRIGGER, value])
        )
        ack = self.arcom.read_uint8()
        
        if ack==1:
            self._trigger_mode = value
        return ack==1
        

    def set_trigger_profiles(self, trigger_profiles):

        length, width = trigger_profiles.shape

        if length!=self.n_trigger_profiles or width!=self.n_channels:
            raise Exception(
                'Error setting trigger profiles: matrix of trigger profiles must be {0} profiles X {1} channels.'.format(
                self.n_trigger_profiles, self.n_channels
            ))

        """ TODO
        if sum(sum((profileMatrix > 0)') > obj.maxSimultaneousChannels) > 0
                error(['Error setting trigger profiles: the current sampling rate only allows ' num2str(obj.maxSimultaneousChannels) ' channels to be triggered simultaneously. Your profile matrix contains at least 1 profile with too many channels.']);
            end
        """
        profile_matrix_out = trigger_profiles
        profile_matrix_out[profile_matrix_out==0] = 256
        
        self.arcom.write_array(
            ArduinoTypes.get_uint8_array([self.COM_LOAD_TRIGGER_PROFILE, profile_matrix_out-1])
        )
        ack = self.arcom.read_uint8()
        
        if ack==1:
            self._trigger_profiles = trigger_profiles
        return ack==1
         
            



    ######################################################################
    ### PROPERTIES #######################################################
    ######################################################################

    
    @property
    def trigger_mode(self):
        return self._trigger_mode
    
    @property
    def bpod_events(self):
        return self._bpod_events
    
    @property
    def loop_mode(self):
        return self._loop_mode
    
    @property
    def loop_duration(self):
        return self._loop_duration
        
    @property
    def trigger_profile_enable(self):
        return self._trigger_profile_enable
    
    @property
    def trigger_profiles(self):
        return self._trigger_profiles
    
    @property
    def output_range(self):
        return self._output_range
    
    @property
    def sampling_rate(self):
        return self._sampling_rate

    @property
    def max_waves(self):
        return self._max_waves
    
    @property
    def n_channels(self):
        return self._n_channels

    @property
    def n_trigger_profiles(self):
        return self._n_trigger_profiles
    

    ######################################################################
    ### PRIVATE FUNCTIONS ################################################
    ######################################################################

    def __get_parameters(self):
        self.arcom.write_array([self.COM_GET_PARAMETERS])

        print('send', self.COM_GET_PARAMETERS)
        # number of output channels
        self._n_channels             = self.arcom.read_uint8()
        # maximum number of waveforms supported
        self._max_waves              = self.arcom.read_uint16()
        # current trigger mode
        self._trigger_mode           = self.arcom.read_uint8()
        # 0 = standard trigger mode, 1 = trigger profile mode
        self._trigger_profile_enable = self.arcom.read_uint8()==1
        # maximum number of trigger profiles supported
        self._n_trigger_profiles     = self.arcom.read_uint8()
        # index of the currently selected range 
        self._output_range           = self.arcom.read_uint8()
        # sampling period (in microseconds)
        sampling_period_microseconds = self.arcom.read_float32()
        # 0 = off, 1 = bpod event reporting
        self._bpod_events   = [v==1 for v in self.arcom.read_uint8_array(self.n_channels)]
        
        # 0 = off, 1 = on
        self._loop_mode     = [v==1 for v in self.arcom.read_uint8_array(self.n_channels)]

        self._sampling_rate = round((1/sampling_period_microseconds)*1000000)

        # duration of loop playback in samples
        self._loop_duration = np.array(self.arcom.read_uint32_array(self.n_channels))*self.sampling_rate
        
        #self.is_playing       = [False for i in range(self.n_channels)]
        self._trigger_profiles = np.zeros( (self.n_trigger_profiles, self.n_channels) )
        



    def __print_parameters(self):
        print('Number of channels:',self.n_channels)
        print('Max waves:',self.max_waves)
        print('Trigger mode:',self.trigger_mode)
        print('Trigger profile enabled:',self.trigger_profile_enable)
        print('Number of trigger profiles:',self.n_trigger_profiles)
        print('Output range:',self.output_range)
        print('Bpod events:',self.bpod_events)
        print('Loop mode',self.loop_mode)
        print('Sampling rates:',self.sampling_rate)
        print('Loop duration:',self.loop_duration)