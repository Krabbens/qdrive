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
                        print(colorama.Fore.LIGHTRED_EX + "[debug] " + colorama.Fore.GREEN + 'Found FUSE folder' + colorama.Fore.RESET)
                        print(colorama.Fore.LIGHTRED_EX + "[debug] " + colorama.Fore.GREEN + 'ID: ' + colorama.Fore.RESET + file['id'])
                    break
        GDriveFileSystem.ls = MonkeyPatch.ls
        self.fs = GDriveFileSystem(self.root["id"], use_service_account=True, client_json_file_path=self.account_path + 'g_fuse_1.json')

    def get_files_for_fuse(self):
        files = []
        for account in self.accounts:
            files.append(account.drive.ListFile({}).GetList())
        return files
    
    def list_files(self):
        return self.fs.listdir('/', detail=True)
    
    

