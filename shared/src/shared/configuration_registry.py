class ConfigurationRegistry:
    def __init__(self):
        self._settings = {}

    def register(self, key: str, settings: object) -> None:
        self._settings[key] = settings

    def get(self, key: str) -> object:
        if key not in self._settings:
            raise KeyError(f"No settings found for key: {key}")
        return self._settings[key]