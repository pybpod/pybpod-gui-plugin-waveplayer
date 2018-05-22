from pybpodapi.bpod_modules.bpod_module import BpodModule


class AnalogOutput(BpodModule):
    
    def __init__(self):
        print('INITING')

    @staticmethod
    def check_module_type(module_name):
        return module_name and module_name.startswith('AnalogOutput')