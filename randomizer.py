import random
# import matplotlib.pyplot as plt

class FingerPresser:
    @staticmethod
    def simulate_press(buttonsize: tuple[tuple, tuple]) -> tuple[float, float]:
        from touch import ClickerAgent
        random.seed(a=None)
        ((x1, y1), (x2, y2)) = buttonsize
        x = random.uniform(x1/2, x2/2)
        y = random.uniform(y1/2, y2/2)
        ClickerAgent.press(x, y)
        return (x, y)

class Randomizer:
    @staticmethod
    def fuzz(value: int, diff: float = 0.05) -> int:
        random.seed(a=None) # uses current time as our seed making it random each time run
        range = value * diff
        return int(random.uniform(value - range, value + range))

'''
rand = Randomizer()
x = 1500
nums = [rand.fuzz(x, 0.05) for _ in range(500)]
plt.hist(nums, bins='auto')
plt.title('Number distribution')

print(f'input value: {x}')
print(f'min value: {min(nums)}')
print(f'max value: {max(nums)}')
plt.show()

'''
