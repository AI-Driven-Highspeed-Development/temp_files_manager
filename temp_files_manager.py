from managers.config_manager import ConfigManager

class TempFilesManager:
    
    def __init__(self):
        self.cm = ConfigManager()
        self.config = self.cm.config.temp_files_manager
        
    def display_module_name(self):
        print("Module Name:", self.config.module_name)