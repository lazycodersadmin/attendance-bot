class Logger:
    def info(self, text):
        print('[*] ', text)

    def warn(self, text):
        print('[!] ', text)

    def success(self, text):
        print('[+] ', text)

    def error(self, text):
        print('[x] ', text)
