import sys

def sum(n):
    ret = 0
    n = int(n)
    for i in range(1, n):
        ret = ret + i
    return ret

if __name__ == "__main__":
    print(sum(sys.argv[1]))

