import sys
file = sys.argv[1]

with open(file, 'r') as f:
    token = f.read()[:-1]
    i = 0
    result = ""

    while i < len(token):
        result = result + chr(ord(token[i]) - i)
        i = i + 1

print(result)