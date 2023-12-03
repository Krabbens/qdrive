from pydrive2.fs import GDriveFileSystem
from .DriveInstance import DriveInstance
from .MonkeyPatch import *
from ..Debug import Debug
import os
import colorama
import sys
from io import BytesIO

debug = len(sys.argv) > 1 and sys.argv[1] == "--debug"


class DriveHandler:
    def __init__(self) -> None:
        self.account_path = os.path.dirname(os.path.realpath(__file__)) + "/Accounts/"
        self.fs = None
        self.accounts = []
        self.root = None
        self.current_path = "/"

    def create_instances(self):
        for file in os.listdir(self.account_path):
            if file.endswith(".json"):
                self.accounts.append(DriveInstance(self.account_path + file))
        l = self.get_files_for_fuse()
        for list in l:
            if self.root != None:
                break
            for file in list:
                if file["title"] == "FUSE":
                    self.root = file
                    Debug()("FUSE:", self.root["id"])
                    break
        GDriveFileSystem.ls = MonkeyPatch.ls
        self.fs = GDriveFileSystem(
            self.root["id"],
            use_service_account=True,
            client_json_file_path=self.account_path + "g_fuse_1.json",
        )

    def get_files_for_fuse(self):
        files = []
        for account in self.accounts:
            files.append(account.drive.ListFile({}).GetList())
        return files

    def list_files(self):
        files = self.fs.listdir(self.current_path, detail=True)
        files = self.combine_parts(files)
        return files

    def combine_parts(self, files):
        new_files = []
        for file in files:
            if ".gpart" in file["name"]:
                Debug()("File:", file["name"])
                found = False
                if len(new_files) > 0:
                    for f in new_files:
                        if f["name"] == file["name"].split(".gpart")[0]:
                            f["size"] = sizeof_fmt(
                                int_size_from_str(file["size"])
                                + int_size_from_str(f["size"])
                            )
                            f["parts"].append(
                                (file["name"].split(".gpart")[1], file["id"])
                            )
                            found = True
                            break
                if not found:
                    file["parts"] = [(file["name"].split(".gpart")[1], file["id"])]
                    file["name"] = file["name"].split(".gpart")[0]
                    file["id"] = "partfile"
                    new_files.append(file)
            else:
                new_files.append(file)
        return new_files

    def open_directory(self, directory):
        if directory == "..":
            self.current_path = self.current_path[:-1]
            self.current_path = self.current_path[: self.current_path.rfind("/") + 1]
            if self.current_path == "/":
                return self.list_files()
        else:
            self.current_path += directory + "/"

        files = [
            {
                "name": "..",
                "type": "directory",
                "icon": "\uf0e2",
                "date": "",
                "size": 0,
                "parentName": self.current_path[:-1],
                "id": "",
            }
        ]
        files.extend(self.fs.listdir(self.current_path, detail=True))
        for f in files:
            f["name"] = f["name"].split("/")[-1]

        files = self.combine_parts(files)

        Debug()("Current path:", self.current_path)
        Debug()("Files:", files)

        return files

    def print_progress(self, progress, total):
        print("Progress: " + str(progress) + " Total: " + str(total))

    def download_file(self, name, id, size, callback):
        Debug()("Downloading file:", id)
        file = self.accounts[0].drive.CreateFile({"id": id})
        _size = 0
        with open("./Downloads/" + name, "ab") as f:
            for chunk in file.GetContentIOBuffer(chunksize=1024 * 1024 * 10):
                callback(_size, size)
                f.write(chunk)
                _size += len(chunk)
        return _size

    def delete_file(self, id):
        Debug()("Delete:", id)
        file = self.accounts[0].drive.CreateFile({"id": id})
        file.Delete()

    def delete_all_files(self):
        for file in self.fs.listdir("/", detail=True):
            self.delete_file(file["id"])
