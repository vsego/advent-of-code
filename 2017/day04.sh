python3 -c 'import sys; print(sum(1 for line in (line.split(" ") for line in sys.stdin.read().splitlines()) if len(set(line)) == len(line)))' < day4.txt 
python3 -c 'import sys; print(sum(1 for line in (["".join(sorted(w)) for w in line.split(" ")] for line in sys.stdin.read().splitlines()) if len(set(line)) == len(line)))' < day4.txt
