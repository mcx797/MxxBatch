import datetime
import json


class MxLog:
    _config_file_path = 'C:/Users/77902/Desktop/LeadingBatch/config/config.json'
    #_config_file_path = 'config/config.json'
    def __init__(self):
        with open(self._config_file_path, encoding='utf-8') as f:
            cfg = json.load(f)
            log_path = cfg['Folders']['Log']
        self._url  = cfg['Folders']['Log']

    @property
    def wrong_url(self):
        return '{}/wrong.log'.format(self._url)

    def wrongLog(self, mes):
        with open(self.wrong_url, 'a', encoding='utf-8') as f:
            f.write('{{ \'time\': {}, \'mes\': {} }}\n'.format(datetime.datetime.now(), mes))
            print('{{ \'datetime\': {}, \'mes\': {} }}'.format(datetime.datetime.now(), mes))


if __name__ == '__main__':
    MxLog().wrongLog('test test!!')

