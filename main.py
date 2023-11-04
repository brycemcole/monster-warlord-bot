import time
import json

QUEST_LOG = 'quests.json'

DEFAULT_ACTIONS = [
    'home',
    'news',
    'quest',
    'battle',
    'monster',
    'equipment',
    'shop'
]

LOCATIONS = {
    'home': 'images/menu-buttons/home-button.png',
    'news': 'images/menu-buttons/news-button.png',
    'quest': 'images/menu-buttons/quest-button.png',
    'battle': 'images/menu-buttons/battle-button.png',
    'monster': 'images/menu-buttons/monster-button.png',
    'equipment': 'images/menu-buttons/equipment-button.png',
    'shop': 'images/menu-buttons/shop-button.png'
}

class MonsterWarlordInstance:
    def __init__(self):
        from vision import ViewAgent
        questmode = 1

        #quest_room = ViewAgent.find_on_screen('images/game-icons/quest-text.png')

        from quest import QuestHandler
        x = QuestHandler('quests.json')
        if questmode:
            


        self.player = dict(ViewAgent.get_user_info())


    @staticmethod
    def press_home():
        from vision import ViewAgent
        from touch import FingerPresser
        button_size = ViewAgent.find_on_screen(LOCATIONS['home'])
        FingerPresser.simulate_press(button_size)


class Node:
    def __init__(self, page_data, actions=[]):
        self.page_data = page_data
        self.children = []
        self.actions = DEFAULT_ACTIONS + actions
        self.parent = None

    def action_possible(self, action):
        return action in self.actions




def main():
    while True:
        game = MonsterWarlordInstance()

        print(game.player)
        time.sleep(2)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
