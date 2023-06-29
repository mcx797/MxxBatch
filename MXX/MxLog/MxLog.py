import datetime
import json


class MxLog:
    def __init__(self):
        self._wrong_url = './config/log/wrong.log'
        self._rename_url = './config/log/rename.log'

    @property
    def wrong_url(self):
        return self._wrong_url

    @property
    def rename_url(self):
        return self._rename_url

    def wrongLog(self, mes):
        with open(self.wrong_url, 'a', encoding='utf-8') as f:
            f.write('{{ \'time\': {}, \'mes\': {} }}\n'.format(datetime.datetime.now(), mes))
            print('{{ \'datetime\': {}, \'mes\': {} }}'.format(datetime.datetime.now(), mes))

    def renameLog(self, path, label, auto_label):
        with open(self.rename_url, 'a', encoding='utf-8') as f:
            f.write('{{\'time\': {}, \'path\':{}, \'label\':{}, \'auto_label\':{} }},\n'.format(datetime.datetime.now(), path, label, auto_label))
            print('{{\'time\': {}, \'path\':{}, \'label\':{}, \'auto_label\':{} }}'.format(datetime.datetime.now(), path, label, auto_label))

if __name__ == '__main__':
    MxLog().wrongLog('test test!!')

