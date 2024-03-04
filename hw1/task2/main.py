import sys

format = '==> %s <=='
tail_upperbound_file  = 10
tail_upperbound_stdin = 17

def GetSufFrom(input, skok):
    return input.readlines()[-skok:]

if len(sys.argv) == 1:
    print(''.join(GetSufFrom(sys.stdin, tail_upperbound_stdin)))
    exit(0)

file_names = sys.argv[1:]
n = len(file_names)
if n == 1:
    print(''.join(GetSufFrom(open(file_names[0]), tail_upperbound_file)), end='')
else:
    for i, file_name in enumerate(file_names):
        print(format % file_name)
        print(''.join(GetSufFrom(open(file_name), tail_upperbound_file)), end='')
        if i + 1 != n:
            print()