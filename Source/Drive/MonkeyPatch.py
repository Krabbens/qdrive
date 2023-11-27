import errno
import os
import posixpath
from datetime import datetime
FOLDER_MIME_TYPE = "application/vnd.google-apps.folder"

class MonkeyPatch:

    def ls(self, path, detail=False):
            bucket, base = self.split_path(path)

            cached = base in self._ids_cache["dirs"]
            if cached:
                dir_ids = self._ids_cache["dirs"][base]
            else:
                dir_ids = self._path_to_item_ids(base)

            if not dir_ids:
                raise FileNotFoundError(
                    errno.ENOENT, os.strerror(errno.ENOENT), path
                )

            root_path = posixpath.join(bucket, base)
            contents = []
            for item in self._gdrive_list_ids(dir_ids):
                item_path = posixpath.join(root_path, item["title"])
                if item["mimeType"] == FOLDER_MIME_TYPE:
                    contents.append(
                        {
                            "type": "directory",
                            "name": item_path.rstrip("/"),
                            "size": 0,
                            "id": item["id"],
                            "parentId": item["parents"][0]["id"],
                            "icon": "\uf07b",
                            "date": datetime.strptime(item["modifiedDate"], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%a %b %y %H:%M")
                        }
                    )
                else:
                    size = item.get("fileSize")
                    contents.append(
                        {
                            "type": "file",
                            "name": item_path,
                            "size": int(size) if size is not None else size,
                            "id": item["id"],
                            "parentId": item["parents"][0]["id"],
                            "icon": "\uf15b",
                            "date": datetime.strptime(item["modifiedDate"], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%a %b %y %H:%M")
                        }
                    )

            if not cached:
                self._cache_path_id(root_path, *dir_ids)

            if detail:
                return contents
            else:
                return [content["name"] for content in contents]