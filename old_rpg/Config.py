class Config:
    def __init__(self, path="config.yaml"):
        import yaml
        with open(path, "r", encoding="utf-8") as f:
            self.data = yaml.safe_load(f)

    def __getitem__(self, key):
        return self.data[key]

    def get(self, *keys, default=None):
        d = self.data
        for key in keys:
            if key in d:
                d = d[key]
            else:
                return default
        return d
