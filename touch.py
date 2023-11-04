import random

import pyautogui


class ClickerAgent:
    @staticmethod
    def press(x, y):
        import logging
        from randomizer import Randomizer
        logging.basicConfig(level=logging.DEBUG)

        randomized_x = Randomizer.fuzz(x)
        randomized_y = Randomizer.fuzz(y)

        pyautogui.click(randomized_x, randomized_y)

        logging.debug(f' x: {randomized_x}, y: {randomized_y}')

class FingerPresser:
    @staticmethod
    def simulate_press(buttonsize: tuple[tuple, tuple]) -> tuple[float, float]:
        random.seed(a=None)
        ((x1, y1), (x2, y2)) = buttonsize
        x = random.uniform(x1/2, x2/2)
        y = random.uniform(y1/2, y2/2)
        ClickerAgent.press(x, y)
        return (x, y)