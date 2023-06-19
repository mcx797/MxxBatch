from mxx.mxxfile.File import File
import datetime

class LogFile(File):
    def __init__(self, file_path):
        super().__init__(file_path = file_path)

    def addLog(self, logContent):
        print(logContent)
        with open(self.filePath(), 'a', encoding='utf-8') as f:
            f.write(str(datetime.datetime.now()) + '\n')
            f.write(logContent + '\n\n')

wrong_log = LogFile('C:\\Users\\77902\\Desktop\\LeadingBatch\\log\\wrong.log')

if __name__ == '__main__':
    file = LogFile('C:\\Users\\77902\\Desktop\\LeadingBatch\\log\\wrong.log')
    file.addLog('test test')