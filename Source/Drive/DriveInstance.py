import sys
import colorama
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials
from ..Debug import Debug


class DriveInstance:
    def __init__(self, auth) -> None:
        self.auth = GoogleAuth()
        self.scope = ["https://www.googleapis.com/auth/drive"]
        self.auth.auth_method = "service"
        self.auth.credentials = ServiceAccountCredentials.from_json_keyfile_name(
            auth, self.scope
        )
        self.drive = GoogleDrive(self.auth)
        if Debug().debug:
            self.get_drive_space()
            self.get_drive_used_space()

    def get_about(self):
        return self.drive.GetAbout()

    def get_drive_space(self):
        about = self.get_about()
        Debug()(
            about["name"].split("@")[0],
            " Drive space: ",
            str(about["quotaBytesTotal"]) + " bytes",
        )
        return about["quotaBytesTotal"]

    def get_drive_used_space(self):
        about = self.get_about()
        Debug()(
            about["name"].split("@")[0],
            " Drive used space: ",
            str(about["quotaBytesUsedAggregate"]) + " bytes",
        )
        return about["quotaBytesUsedAggregate"]
