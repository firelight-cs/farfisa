import json
import os

class PromptComposer:
    def __init__(self, json_data: dict, template: str=" "):
        self.data = json_data
        self.template = template

    def compose_prompt(self):
        description = self.data.get("description", "")
        if not self.template:
            return description
        try:
            return self.template.format(description=description)
        except Exception:
            return f'{self.template}{description}'


    # manually load json in case it wasn't loaded via GUI call
    @classmethod
    def from_json_file(cls, filepath:str, template: str=""):
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls(data, template)

