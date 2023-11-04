from vision import ViewAgent
import os
import json

class Quest:
    def __init__(self, name, rewards, xp, stamina_required):
        self.name = name
        self.rewards = rewards
        self.xp = xp
        self.stamina_required = stamina_required

    def __repr__(self):
        return f"Quest(name={self.name}, rewards={self.rewards}, xp={self.xp}, stamina_required={self.stamina_required})"

class Area:
    def __init__(self, name):
        self.name = name
        self.quests = {}

    def add_quest(self, quest):
        self.quests[quest.name] = quest

    def get_quest_info(self, quest_name):
        return self.quests.get(quest_name, None)

class QuestHandler:
    def __init__(self, file_path, default_data=None):
        self.quests = {}
        self.file_path = file_path
        self.default_data = default_data
        self.handle_json_data()

    def handle_json_data(self):
        if not os.path.isfile(self.file_path):
            with open(self.file_path, 'w') as file:
                json.dump(self.default_data or {}, file)
                return self.default_data or {}
        else:
            with open(self.file_path, 'r') as file:
                a = json.load(file)
                self.quests = dict(a)
                return a
