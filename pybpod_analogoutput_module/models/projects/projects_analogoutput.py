from pyforms import conf
from AnyQt.QtGui import QIcon

from pybpod_analogoutput_module.module_gui import AnalogOutputModuleGUI

class ProjectsAnalogOutput(object):

	def register_on_main_menu(self, mainmenu):
		super(ProjectsAnalogOutput, self).register_on_main_menu(mainmenu)

		if len([m for m in mainmenu if 'Tools' in m.keys()]) == 0:
			mainmenu.append({'Tools': []})

		menu_index = 0
		for i, m in enumerate(mainmenu):
			if 'Tools' in m.keys(): menu_index=i; break

		mainmenu[menu_index]['Tools'].append( '-' )	
		mainmenu[menu_index]['Tools'].append( {'Analog Output': self.open_analogoutput_plugin, 'icon': QIcon(conf.ROTARYENCODER_PLUGIN_ICON)})
	
	def open_analogoutput_plugin(self):
		if not hasattr(self, 'rotaryencoder_plugin'):
			self.analogoutput_plugin = AnalogOutputModuleGUI(self)
			self.analogoutput_plugin.show()
			#self.rotaryencoder_plugin.resize(*conf.ROTARYENCODER_PLUGIN_WINDOW_SIZE)			
		else:
			self.analogoutput_plugin.show()

		return self.analogoutput_plugin