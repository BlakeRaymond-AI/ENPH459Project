__author__ = 'Blake'

import time
import math


def main():
    count = 3

    while True:
        isprime = True

        for x in range(2, int(math.sqrt(count) + 1)):
            if count % x == 0:
                isprime = False
                break

        if isprime:
            print count
            time.sleep(0.1)

        count += 1


main()
