import subprocess

def open_file(url):
    subprocess.Popen('start {} '.format(url), shell=True)