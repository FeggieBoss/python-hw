import sys

format = '%6d\t%s'

input = sys.stdin

if len(sys.argv) > 1:
    input = open(sys.argv[1])

for i, line in enumerate(input):
    print(format % (i + 1, line), end='')
print()