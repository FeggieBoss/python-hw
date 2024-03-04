import sys
import os
import math

format_stdin  = '%7d %7d %7d'
format_file   = '%*d %*d %*d %s'
w = 1

def get_wc(input): # (lines, words, bytes)
    bytes = input.read()
    return (len(bytes.split('\n'))-1,len(bytes.split()),len(bytes))

if len(sys.argv) == 1:
    print(format_stdin % get_wc(sys.stdin))
    exit(0)

file_names = sys.argv[1:]
n = len(file_names)

summary_size = 0
for f in file_names:
    summary_size += os.path.getsize(f)
w += int(math.log10(summary_size))

summary_lines = 0
summary_words = 0
summary_bytes = 0
for file_name in file_names:
    ls, ws, bs = get_wc(open(file_name))
    print(format_file % (w, ls, w, ws, w, bs,file_name))
    summary_lines += ls
    summary_words += ws
    summary_bytes += bs

if n > 1:
    print(format_file % (w, summary_lines, w, summary_words, w, summary_bytes, 'total'))
