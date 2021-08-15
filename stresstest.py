from random import choices
from time import time

from delimiter_check import get_results_from_file

alphabet = [
        "a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
        "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
        "u", "v", "w", "x", "y", "z", "0", "1", "2", "3",
        "4", "5", "6", "7", "8", "9", "(", ")", "[", "]",
        "{", "}"
]

print("Creating file for the stress test.")
with open('testing_file', 'w') as outfile:
    for i in range(100000):
        line = ''.join(choices(alphabet, k=80))
        outfile.write(line + '\n')

print('Created the file. Now on to the stress test.')

start = time()

with open('testing_file', 'r') as infile:
    result = get_results_from_file(infile)

end = time()

print(f'''Stress test complete. It took
    {end - start}
seconds. You may now close the temporary testing file.''')
