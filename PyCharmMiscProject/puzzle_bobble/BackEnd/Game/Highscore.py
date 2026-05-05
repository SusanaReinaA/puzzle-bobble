class Highscore:
    def __init__(self, filepath="highscore.txt"):
        self.filepath = filepath
        self.highscore = self._load()

    def _load(self):
        try:
            with open(self.filepath, "r") as f:
                return int(f.read())
        except:
            return 0

    def save(self, score):
        if score > self.highscore:
            self.highscore = score
            with open(self.filepath, "w") as f:
                f.write(str(score))

    def get(self):
        return self.highscore