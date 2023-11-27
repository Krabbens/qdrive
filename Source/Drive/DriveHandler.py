from pydrive2.fs import GDriveFileSystem
from .DriveInstance import DriveInstance
from .MonkeyPatch import MonkeyPatch
import os
import colorama
import sys

debug = len(sys.argv) > 1 and sys.argv[1] == '--debug'

class DriveHandler():
    def __init__(self) -> None:
        self.account_path = os.path.dirname(os.path.realpath(__file__)) + '/Accounts/'
        self.fs = None
        self.accounts = []
        self.root = None
        self.current_path = "/"

    def create_instances(self):
        for file in os.listdir(self.account_path):
            if file.endswith('.json'):
                self.accounts.append(DriveInstance(self.account_path + file))
        l = self.get_files_for_fuse()
        for list in l:
            if self.root != None: break
            for file in list:
                if file['title'] == 'FUSE':
                    self.root = file
                    if debug:
                        print(colorama.Fore.LIGHTRED_EX + "[debug] DriveHandler " + colorama.Fore.GREEN + 'FUSE: ' + colorama.Fore.RESET + self.root["id"])
                    break
        GDriveFileSystem.ls = MonkeyPatch.ls
        self.fs = GDriveFileSystem(self.root["id"], use_service_account=True, client_json_file_path=self.account_path + 'g_fuse_1.json')

    def get_files_for_fuse(self):
        files = []
        for account in self.accounts:
            files.append(account.drive.ListFile({}).GetList())
        return files
    
    def list_files(self):
        return self.fs.listdir(self.current_path, detail=True)
    
    def open_directory(self, directory):
        if directory == '..':
            self.current_path = self.current_path[:-1]
            self.current_path = self.current_path[:self.current_path.rfind('/') + 1]
            if self.current_path == '/':
                return self.list_files()
        else:
            self.current_path += directory + '/'

        files = [{'name': '..', 'type': 'directory', 'icon': '\uf0e2', 'date': '', 'size': 0}]
        files.extend(self.fs.listdir(self.current_path, detail=True))
        for f in files:
            f['name'] = f['name'].split('/')[-1]
        if debug:
            print(colorama.Fore.LIGHTRED_EX + "[debug] DriveHandler " + colorama.Fore.GREEN + 'Current path: ' + colorama.Fore.RESET + self.current_path)
            print(colorama.Fore.LIGHTRED_EX + "[debug] DriveHandler " + colorama.Fore.GREEN + 'Files: ' + colorama.Fore.RESET + str(files))
        
        return files

