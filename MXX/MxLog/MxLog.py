import datetime
import json


class MxLog:
    def __init__(self):
       self._wrong_url = './config/log/wrong.log'

    @property
    def wrong_url(self):
        return self._wrong_url

    def wrongLog(self, mes):
        with open(self.wrong_url, 'a', encoding='utf-8') as f:
            f.write('{{ \'time\': {}, \'mes\': {} }}\n'.format(datetime.datetime.now(), mes))
            print('{{ \'datetime\': {}, \'mes\': {} }}'.format(datetime.datetime.now(), mes))


if __name__ == '__main__':
    MxLog().wrongLog('test test!!')

