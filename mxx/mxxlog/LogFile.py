from mxx.mxxfile.File import File
from app.common.config import cfg
import datetime

class LogFile(File):
    def __init__(self, file_path):
        super().__init__(file_path = file_path)

    def addLog(self, logContent):
        print(logContent)
        with open(self.filePath(), 'a', encoding='utf-8') as f:
            f.write(str(datetime.datetime.now()) + '\n')
            f.write(logContent + '\n\n')

url = cfg.get(cfg.logFolder)
wrong_url = url + '\\wrong.log'
wrong_log = LogFile(wrong_url)
auto_url = url + '\\auto.log'
auto_log = LogFile(auto_url)

if __name__ == '__main__':
    url = cfg.get(cfg.logFolder)
    print(url)
    file = LogFile('C:\\Users\\77902\\Desktop\\LeadingBatch\\config\\log\\wrong.log')
    file.addLog('test test')