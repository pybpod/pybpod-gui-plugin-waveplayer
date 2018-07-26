import pyforms
from pyforms import BaseWidget
from pyforms.controls import ControlLabel, ControlText, ControlButton, ControlCombo, ControlCheckBox, ControlFile
from pybpod_analogoutput_module.module_api import AnalogOutputModule


class AnalogOutputModuleGUI(AnalogOutputModule, BaseWidget):

    TITLE = 'Analog Output Module'

    def __init__(self, parent_win = None):
        BaseWidget.__init__(self, self.TITLE, parent_win = parent_win)
        AnalogOutputModule.__init__(self)

        self._port 			= ControlText('Serial port', default = '/dev/tty.usbmodem3751351')
        self._connect_btn   = ControlButton('Connect', checkable=False, default = self.connect)
        self._get_status_btn   = ControlButton('Get Parameters', checkable=False, default = self.getparams)
        self._select_wave_btn = ControlFile('Select Waveform')
        self._ch_select_combo = ControlCombo('Select Channel')
        self._load_waveform_btn = ControlButton('Load Waveform', default = self.loadWaveform)
        self._set_sampling_rate_btn = ControlButton('Set',default = self.setTimerPeriod)
        self._trigger_mode = ControlCombo('Channel Select')
        self._output_range = ControlCombo()
        self._timer_period = ControlText('Timer Period')
        self._connection_status = ControlLabel('Not Connected')
        self._channel_name_lbl = ControlLabel('Channel Name')
        self._report_lbl = ControlLabel('Event Reporting')
        self._loop_mode_lbl = ControlLabel('Loop Mode')
        self._loop_duration_lbl = ControlLabel('Loop Duration')
        self._channel_name_lbl2 = ControlLabel('Channel Name')
        self._report_lbl2 = ControlLabel('Event Reporting')
        self._loop_mode_lbl2 = ControlLabel('Loop Mode')
        self._loop_duration_lbl2 = ControlLabel('Loop Duration')
        self._channel_name_ch1 = ControlLabel('CH1')
        self._channel_name_ch2 = ControlLabel('CH2')
        self._channel_name_ch3 = ControlLabel('CH3')
        self._channel_name_ch4 = ControlLabel('CH4')
        self._channel_name_ch5 = ControlLabel('CH5')
        self._channel_name_ch6 = ControlLabel('CH6')
        self._channel_name_ch7 = ControlLabel('CH7')
        self._channel_name_ch8 = ControlLabel('CH8')
        self._event_report_ch1 = ControlCheckBox()
        self._event_report_ch2 = ControlCheckBox()
        self._event_report_ch3 = ControlCheckBox()
        self._event_report_ch4 = ControlCheckBox()
        self._event_report_ch5 = ControlCheckBox()
        self._event_report_ch6 = ControlCheckBox()
        self._event_report_ch7 = ControlCheckBox()
        self._event_report_ch8 = ControlCheckBox()
        self._loop_mode_ch1 = ControlCheckBox()
        self._loop_mode_ch2 = ControlCheckBox()
        self._loop_mode_ch3 = ControlCheckBox()
        self._loop_mode_ch4 = ControlCheckBox()
        self._loop_mode_ch5 = ControlCheckBox()
        self._loop_mode_ch6 = ControlCheckBox()
        self._loop_mode_ch7 = ControlCheckBox()
        self._loop_mode_ch8 = ControlCheckBox()
        self._loop_duration_ch1 = ControlText()
        self._loop_duration_ch2 = ControlText()
        self._loop_duration_ch3 = ControlText()
        self._loop_duration_ch4 = ControlText()
        self._loop_duration_ch5 = ControlText()
        self._loop_duration_ch6 = ControlText()
        self._loop_duration_ch7 = ControlText()
        self._loop_duration_ch8 = ControlText()

        # play section
        self._play_btn = ControlButton('Play', default = self._play)
        self._stop_btn = ControlButton('Stop',default = self._stop)
        self._play_ch1 = ControlCheckBox('CH1')
        self._play_ch2 = ControlCheckBox('CH2')
        self._play_ch3 = ControlCheckBox('CH3')
        self._play_ch4 = ControlCheckBox('CH4')
        self._play_ch5 = ControlCheckBox('CH5')
        self._play_ch6 = ControlCheckBox('CH6')
        self._play_ch7 = ControlCheckBox('CH7')
        self._play_ch8 = ControlCheckBox('CH8')
        self._play_slotselect = ControlCombo()


        self.set_margin(10)

        self._trigger_mode += 'Standard Mode'
        self._trigger_mode += 'Trigger Profile'

        self._output_range += '0V to +5V'
        self._output_range += '0V to +10V'
        self._output_range += '0V to +12V'
        self._output_range += '-5V to +5V'
        self._output_range += '-10V to +10V'
        self._output_range += '-12V to +12V'

        self._output_range.changed_event = self.setOutputRange
        self._trigger_mode.changed_event = self.setTriggerMode
        #self._timer_period.changed_event = self.setTimerPeriod

        self._get_status_btn.enabled = False
        self._trigger_mode.enabled = False
        self._output_range.enabled = False

        self._event_report_ch8.enabled = False
        self._event_report_ch7.enabled = False
        self._event_report_ch6.enabled = False
        self._event_report_ch5.enabled = False
        self._event_report_ch4.enabled = False
        self._event_report_ch3.enabled = False
        self._event_report_ch2.enabled = False
        self._event_report_ch1.enabled = False
        self._loop_duration_ch4.enabled = False
        self._loop_duration_ch3.enabled = False
        self._loop_duration_ch2.enabled = False
        self._loop_duration_ch1.enabled = False
        self._loop_duration_ch8.enabled = False
        self._loop_duration_ch7.enabled = False
        self._loop_duration_ch6.enabled = False
        self._loop_duration_ch5.enabled = False
        self._loop_mode_ch4.enabled = False
        self._loop_mode_ch3.enabled = False
        self._loop_mode_ch2.enabled = False
        self._loop_mode_ch1.enabled = False
        self._loop_mode_ch8.enabled = False
        self._loop_mode_ch7.enabled = False
        self._loop_mode_ch6.enabled = False
        self._loop_mode_ch5.enabled = False

        self._play_ch8.enabled = False
        self._play_ch7.enabled = False
        self._play_ch6.enabled = False
        self._play_ch5.enabled = False
        self._play_ch4.enabled = False
        self._play_ch3.enabled = False
        self._play_ch2.enabled = False
        self._play_ch1.enabled = False
        self._play_btn.enabled = False
        self._play_slotselect.enabled = False

        self._ao_ch1 = 0b00000001
        self._ao_ch2 = 0b00000010
        self._ao_ch3 = 0b00000100
        self._ao_ch4 = 0b00001000
        self._ao_ch5 = 0b00010000
        self._ao_ch6 = 0b00100000
        self._ao_ch7 = 0b01000000
        self._ao_ch8 = 0b10000000

        for i in range(64):
            self._ch_select_combo.add_item(str(i))
            self._play_slotselect.add_item(str(i))

        self.formset = [
            {
                'A:Connection' :[
                    ('_port','_connect_btn'),
                    '_connection_status',
                    '_get_status_btn',
                    '_trigger_mode',
                    '_report_lbl',
                    '_output_range',
                    ('_timer_period','_set_sampling_rate_btn'),
                    ('_ch_select_combo','_select_wave_btn', '_load_waveform_btn'),
                    ],
                'B: Play' : [
                    ('_play_ch1',
                    '_play_ch2',
                    '_play_ch3',
                    '_play_ch4'),
                    ('_play_ch5',
                    '_play_ch6',
                    '_play_ch7',
                    '_play_ch8',
                    ),
                    ('_play_slotselect','_play_btn','_stop_btn')
                    ],
                'C:Channel Settings (1-4)' :[
                    ('_channel_name_lbl','_channel_name_ch1','_channel_name_ch2',
                    '_channel_name_ch3','_channel_name_ch4'),
                    ('_report_lbl','_event_report_ch1','_event_report_ch2',
                    '_event_report_ch3','_event_report_ch4'),
                    ('_loop_mode_lbl','_loop_mode_ch1','_loop_mode_ch2',
                    '_loop_mode_ch3','_loop_mode_ch4'),
                    ('_loop_duration_lbl','_loop_duration_ch1','_loop_duration_ch2',
                    '_loop_duration_ch3','_loop_duration_ch4')
                    ],
                'D:Channel Settings (5-8)' :[
                    ('_channel_name_lbl2','_channel_name_ch5','_channel_name_ch6',
                    '_channel_name_ch7','_channel_name_ch8'),
                    ('_report_lbl2','_event_report_ch5','_event_report_ch6',
                    '_event_report_ch7','_event_report_ch8'),
                    ('_loop_mode_lbl2','_loop_mode_ch5','_loop_mode_ch6',
                    '_loop_mode_ch7','_loop_mode_ch8'),
                    ('_loop_duration_lbl2','_loop_duration_ch5','_loop_duration_ch6',
                    '_loop_duration_ch7','_loop_duration_ch8')
                    ]
            }
        ]


    def _stop(self):
        self.stop()

    def before_close_event(self):
        self.disconnect()
        super(AnalogOutputModuleGUI,self).close()

    def connect(self):
        result = self.open(self._port.value)
        if result:
            self._connection_status.value = 'Connected'
            self._get_status_btn.enabled = True
            self._trigger_mode.enabled = True
            self._output_range.enabled = True
            self.getparams()
            self.activate_signals()

    def activate_signals(self):
        self._event_report_ch8.changed_event = self.setStateMarchineReporting
        self._event_report_ch7.changed_event = self.setStateMarchineReporting
        self._event_report_ch6.changed_event = self.setStateMarchineReporting
        self._event_report_ch5.changed_event = self.setStateMarchineReporting
        self._event_report_ch4.changed_event = self.setStateMarchineReporting
        self._event_report_ch3.changed_event = self.setStateMarchineReporting
        self._event_report_ch2.changed_event = self.setStateMarchineReporting
        self._event_report_ch1.changed_event = self.setStateMarchineReporting

        self._loop_duration_ch8.changed_event = self.setLoop
        self._loop_duration_ch7.changed_event = self.setLoop
        self._loop_duration_ch6.changed_event = self.setLoop
        self._loop_duration_ch5.changed_event = self.setLoop
        self._loop_duration_ch4.changed_event = self.setLoop
        self._loop_duration_ch3.changed_event = self.setLoop
        self._loop_duration_ch2.changed_event = self.setLoop
        self._loop_duration_ch1.changed_event = self.setLoop

        self._loop_mode_ch8.changed_event = self.setLoop
        self._loop_mode_ch7.changed_event = self.setLoop
        self._loop_mode_ch6.changed_event = self.setLoop
        self._loop_mode_ch5.changed_event = self.setLoop
        self._loop_mode_ch4.changed_event = self.setLoop
        self._loop_mode_ch3.changed_event = self.setLoop
        self._loop_mode_ch2.changed_event = self.setLoop
        self._loop_mode_ch1.changed_event = self.setLoop

    def getparams(self):
        # we will use the params variable to set everything in the interface
        params = self.get_parameters()
        self._params = params.copy()
        self._output_range.current_index = params['rangeIndex']
        self._trigger_mode.current_index = params['triggerMode']
        self._timer_period.value = str(params['timerPeriod'])
        # Enable just the channels we need
        if params['nChannels'] > 0:
            self._event_report_ch4.enabled = True
            self._event_report_ch3.enabled = True
            self._event_report_ch2.enabled = True
            self._event_report_ch1.enabled = True
            self._loop_mode_ch4.enabled = True
            self._loop_mode_ch3.enabled = True
            self._loop_mode_ch2.enabled = True
            self._loop_mode_ch1.enabled = True
            self._loop_duration_ch4.enabled = True
            self._loop_duration_ch3.enabled = True
            self._loop_duration_ch2.enabled = True
            self._loop_duration_ch1.enabled = True
            
            self._loop_duration_ch1.value = str(params['loopDuration'][0])
            self._loop_duration_ch2.value = str(params['loopDuration'][1])
            self._loop_duration_ch3.value = str(params['loopDuration'][2])
            self._loop_duration_ch4.value = str(params['loopDuration'][3])

            self._loop_mode_ch1.value = True if params['loopMode'][0] == 1 else False
            self._loop_mode_ch2.value = True if params['loopMode'][1] == 1 else False
            self._loop_mode_ch3.value = True if params['loopMode'][2] == 1 else False
            self._loop_mode_ch4.value = True if params['loopMode'][3] == 1 else False

            self._event_report_ch1.value = True if params['sendBpodEvents'][0] == 1 else False
            self._event_report_ch2.value = True if params['sendBpodEvents'][1] == 1 else False
            self._event_report_ch3.value = True if params['sendBpodEvents'][2] == 1 else False
            self._event_report_ch4.value = True if params['sendBpodEvents'][3] == 1 else False

            self._play_ch4.enabled = True
            self._play_ch3.enabled = True
            self._play_ch2.enabled = True
            self._play_ch1.enabled = True
            self._play_btn.enabled = True
            self._play_slotselect.enabled = True

        if params['nChannels'] > 4:
            self._event_report_ch8.enabled = True
            self._event_report_ch7.enabled = True
            self._event_report_ch6.enabled = True
            self._event_report_ch5.enabled = True
            self._loop_mode_ch8.enabled = True
            self._loop_mode_ch7.enabled = True
            self._loop_mode_ch6.enabled = True
            self._loop_mode_ch5.enabled = True
            self._loop_duration_ch8.enabled = True
            self._loop_duration_ch7.enabled = True
            self._loop_duration_ch6.enabled = True
            self._loop_duration_ch5.enabled = True

            self._play_ch8.enabled = True
            self._play_ch7.enabled = True
            self._play_ch6.enabled = True
            self._play_ch5.enabled = True
            
            self._loop_duration_ch5.value = str(params['loopDuration'][4])
            self._loop_duration_ch6.value = str(params['loopDuration'][5])
            self._loop_duration_ch7.value = str(params['loopDuration'][6])
            self._loop_duration_ch8.value = str(params['loopDuration'][7])

            self._loop_mode_ch5.value = True if params['loopMode'][4] == 1 else False
            self._loop_mode_ch6.value = True if params['loopMode'][5] == 1 else False
            self._loop_mode_ch7.value = True if params['loopMode'][6] == 1 else False
            self._loop_mode_ch8.value = True if params['loopMode'][7] == 1 else False

            self._event_report_ch5.value = True if params['sendBpodEvents'][4] == 1 else False
            self._event_report_ch6.value = True if params['sendBpodEvents'][5] == 1 else False
            self._event_report_ch7.value = True if params['sendBpodEvents'][6] == 1 else False
            self._event_report_ch8.value = True if params['sendBpodEvents'][7] == 1 else False
            
            
    def setOutputRange(self):
        print('setting output range')
        self.set_output_range(self._output_range.current_index)

    def setTriggerMode(self):
        self.set_trigger_mode(self._trigger_mode.current_index)

    def setStateMarchineReporting(self):
        aux = []
        aux.append(1 if self._event_report_ch1.value == True else 0)
        aux.append(1 if self._event_report_ch2.value == True else 0)
        aux.append(1 if self._event_report_ch3.value == True else 0)
        aux.append(1 if self._event_report_ch4.value == True else 0)
        if self._params['nChannels'] > 4:
            aux.append(1 if self._event_report_ch5.value == True else 0)
            aux.append(1 if self._event_report_ch6.value == True else 0)
            aux.append(1 if self._event_report_ch7.value == True else 0)
            aux.append(1 if self._event_report_ch8.value == True else 0)
        
        self.set_state_machine_reporting(aux)

    def setLoop(self):
        print('loop')
        aux = []
        aux2 = []
        aux.append(1 if self._loop_mode_ch1.value == True else 0)
        aux.append(1 if self._loop_mode_ch2.value == True else 0)
        aux.append(1 if self._loop_mode_ch3.value == True else 0)
        aux.append(1 if self._loop_mode_ch4.value == True else 0)
        aux2.append(int(self._loop_duration_ch1.value))
        aux2.append(int(self._loop_duration_ch2.value))
        aux2.append(int(self._loop_duration_ch3.value))
        aux2.append(int(self._loop_duration_ch4.value))
        if self._params['nChannels'] > 4:
            aux.append(1 if self._loop_mode_ch5.value == True else 0)
            aux.append(1 if self._loop_mode_ch6.value == True else 0)
            aux.append(1 if self._loop_mode_ch7.value == True else 0)
            aux.append(1 if self._loop_mode_ch8.value == True else 0)
            aux2.append(int(self._loop_duration_ch5.value))
            aux2.append(int(self._loop_duration_ch6.value))
            aux2.append(int(self._loop_duration_ch7.value))
            aux2.append(int(self._loop_duration_ch8.value))

        self.set_loop(aux,aux2)

    def setTimerPeriod(self):
        print('setting sampling period',int(self._timer_period.value))
        result = self.set_sampling_period(int(self._timer_period.value))
        print ('result',result)


    def loadWaveform(self):
        channel_no = self._ch_select_combo.current_index
        filename = self._select_wave_btn.value
        nsamples = self._load_waveform(filename,channel_no)

        if nsamples != self._params['timerPeriod']:
            #print('frequencies are different',nsamples,self._params['timerPeriod'])
            rpl = self.question('Bpod Analog Output Module has a different sample rate than the last imported waveform. Adjust Module sample rate to match the imported waveform?')
            if rpl == 'yes':
                self._timer_period.value = str(nsamples)
                self.setTimerPeriod()

    
    def _play(self):
        ch_to_play = 0b00000000
        ch_to_play = ch_to_play | self._ao_ch1 if self._play_ch1.value == True else ch_to_play
        ch_to_play = ch_to_play | self._ao_ch2 if self._play_ch2.value == True else ch_to_play
        ch_to_play = ch_to_play | self._ao_ch3 if self._play_ch3.value == True else ch_to_play
        ch_to_play = ch_to_play | self._ao_ch4 if self._play_ch4.value == True else ch_to_play
        ch_to_play = ch_to_play | self._ao_ch5 if self._play_ch5.value == True else ch_to_play
        ch_to_play = ch_to_play | self._ao_ch6 if self._play_ch6.value == True else ch_to_play
        ch_to_play = ch_to_play | self._ao_ch7 if self._play_ch7.value == True else ch_to_play
        ch_to_play = ch_to_play | self._ao_ch8 if self._play_ch8.value == True else ch_to_play
        print('channels to play:',bin(ch_to_play))
        wav_to_play = self._play_slotselect.current_index
        print('wave to play:',wav_to_play)
        
        self.play(ch_to_play,wav_to_play)
        

