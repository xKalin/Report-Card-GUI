import json

from settings import DST_PATH


class Downloader:

    def __init__(self):
        self.path = DST_PATH
        self.dst = self.load_dst_json()

    def load_dst_json(self):
        with open(self.path) as f:
            dst = json.load(f)
        if 'download_path' not in dst:
            return None
        return dst

    def save(self, dst):
        if self.dst is None:
            self.dst = {}
        self.dst['download_path'] = dst
        with open(self.path, "w") as f:
            json.dump(self.dst, fp=f, ensure_ascii=False, indent=4)