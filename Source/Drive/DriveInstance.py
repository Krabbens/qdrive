from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials

class DriveInstance:
    def __init__(self, auth) -> None:
        self.auth = GoogleAuth()
        self.scope = ["https://www.googleapis.com/auth/drive"]
        self.auth.auth_method = 'service'
        self.auth.credentials = ServiceAccountCredentials.from_json_keyfile_name(auth, self.scope)
        self.drive = GoogleDrive(self.auth)

    def get_about(self):
        return self.drive.GetAbout()