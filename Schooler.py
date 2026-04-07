import json
import os
from datetime import datetime


class Schooler:
    def __init__(self):
        self.schedule = {}
        self.homeworks = {}
        self.useful_links = []
        self.data_file = 'school_data.json'
        self.load_data()

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.schedule = data.get("schedule", {})
                self.homeworks = data.get("homeworks", {})
                self.useful_links = data.get("useful_links", [])

        else:
            pass  # значения по умолчанию
            self.save_data()

    def save_data(self):
        data = {
            'schedule': self.schedule,
            'homeworks': self.homeworks,
            'useful_links': self.useful_links,
        }
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

