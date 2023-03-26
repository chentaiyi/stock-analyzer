
import json
import os.path as path

class Singleton(object):
    def __init__(self, cls):
        self._cls = cls
        self._instance = {}
    def __call__(self):
        if self._cls not in self._instance:
            self._instance[self._cls] = self._cls()
        return self._instance[self._cls]

@Singleton
class Configure:

    def __init__(self):
        self.configure = {}

    def _read_config(self,config_file: str) -> dict:
        if path.exists(config_file):
            with open(config_file, "r") as config_file_r:
                return json.loads(config_file_r.read())
        return {}


    def _write_config(self,config_file: str, content: dict) -> None:
        # create config content before opening file not to clear file or json dump exception
        #config_content = configuration.dump_formatted_json(content)
         with open(config_file, "w+") as config_file_w:
            config_file_w.write(content)

    def get_config(self,path='config.json'):
        self.configure = self._read_config(path)
        return self.configure

if __name__=="__main__":
     config = Configure()
     config2 = Configure()
     print(id(config) ==id(config2))
     config.get_config()
     print(config.configure)