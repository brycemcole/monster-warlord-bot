import re
from concurrent.futures import ThreadPoolExecutor

import cv2
import numpy as np
import pytesseract
from PIL import ImageGrab


# lets see lol

class ViewAgent:

    @staticmethod
    def process_template(stat, template_file, screen):
        template = cv2.imread(template_file, 0)
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        return stat, res, w, h
    @staticmethod
    def parse_text(stat, text):
        if stat == 'level':
            # Assuming level is just a number
            return int(re.search(r'\d+', text).group())
        elif stat in ('health', 'energy', 'stamina'):
            # Format "100/100" or just "100"
            match = re.search(r'(\d+)(?:/\d+)?', text.replace(',', ''))
            return int(match.group(1)) if match else None
        elif stat in ('jewels', 'money'):
            # Format "100,000,000"
            return int(text.replace(',', ''))
        else:
            # Default handler
            return text.strip()

    @staticmethod
    def get_user_info():
        file_locations = {
            'level': 'images/game-icons/class-icon.png',
            'exp': 'images/game-icons/class-icon.png',
            'jewels': 'images/game-icons/jewel-icon.png',
            'money': 'images/game-icons/money-icon.png',
            'health': 'images/game-icons/health-icon.png',
            'energy': 'images/game-icons/energy-icon.png',
            'stamina': 'images/game-icons/stamina-icon.png',
        }
        screen = np.array(ImageGrab.grab(bbox=None))
        gray_screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(ViewAgent.process_template, stat, file_dir, gray_screen) for stat, file_dir in file_locations.items()]

        for future in futures:
            stat, res, w, h = future.result()
            threshold = 0.8
            loc = np.where(res >= threshold)

            if loc[0].size == 0:
                print(f'No matches for {stat}')
                continue

            pt = max(zip(*loc[::-1]), key=lambda x: res[x[1], x[0]])
            icon_end_x = pt[0] + w
            roi = None

            if stat == 'level':
                roi = screen[pt[1]:pt[1] + h-37, icon_end_x:icon_end_x + 120]
                cv2.rectangle(screen, (icon_end_x, pt[1]), (icon_end_x + 120, pt[1] + h - 37), (255, 0, 0), 1)
            if stat == 'exp':
                roi = screen[pt[1]+70:pt[1] + h+30, icon_end_x:icon_end_x + 350]
                #cv2.rectangle(screen, (icon_end_x, pt[1] + 70), (icon_end_x + 300, pt[1] + h + 30), (255, 0, 0), 1)
            elif stat in ('health', 'energy', 'stamina'):
                roi = screen[pt[1]:pt[1] + h-30, icon_end_x:icon_end_x + 250]
                #cv2.rectangle(screen, (icon_end_x, pt[1]), (icon_end_x + 250, pt[1] + h-30), (255, 0, 0), 1)
            elif stat == 'jewels':
                roi = screen[pt[1]+20:pt[1]+h-10, icon_end_x:icon_end_x + 200]
                #cv2.rectangle(screen, (icon_end_x, pt[1]+20), (icon_end_x + 200, pt[1] + h-10), (255, 0, 0), 1)
            elif stat == 'money':
                roi = screen[pt[1]:pt[1] + h-20, icon_end_x:icon_end_x + 400]
                #cv2.rectangle(screen, (icon_end_x, pt[1]), (icon_end_x + 400, pt[1] + h-20), (255, 0, 0), 1)

            roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            text = pytesseract.image_to_string(roi_gray)
            parsed_text = ViewAgent.parse_text(stat, text)

            yield stat, parsed_text

        #cv2.imshow('Detected icons & ROIs', screen)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
    @staticmethod
    def find_on_screen(filename: np.array, flags: str = None):

        template = cv2.imread(filename, 0)

        while True:
            screen = np.array(ImageGrab.grab(bbox=None))
            gray_screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

            w, h = template.shape[::-1]

            res = cv2.matchTemplate(gray_screen, template, cv2.TM_CCOEFF_NORMED)
            threshold = 0.8
            loc = np.where(res >= threshold)

            button_sizes = []

            for pt in zip(*loc[::-1]):
                button_size = (pt, (pt[0] + w, pt[1] + h))

                button_sizes.append(button_size)

                # Draw a rectangle on the screenshot
                # - screen is the source image.
                # - top_left is the top-left corner of the rectangle.
                # - bottom_right is the bottom-right corner of the rectangle.
                # - (0, 255, 0) is the rectangle color (green here).
                # - 2 is the thickness of the rectangle lines.
                # cv2.rectangle(screen, top_left, bottom_right, (0, 255, 0), 2)
                # print(top_left)
                # print(bottom_right)
            return button_sizes
