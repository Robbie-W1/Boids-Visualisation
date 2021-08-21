import random
import matplotlib.pyplot as plt
from p5 import noise


def main():
    plt.plot([noise(i/100) for i in range(1000)])
    plt.show()


if __name__ == "__main__":
    main()
