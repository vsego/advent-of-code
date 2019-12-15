#!/usr/bin/bash

set -euo pipefail

day="$(printf "%02d" "$((1+$(ls day*.in | sort | tail -1 | sed -r 's/day([0-9]+)\.in/\1/')))")"

mv /tmp/input.txt "day$day.in"
cat <<EOT > "day$day.py"
#!/usr/bin/env python3


def read_input(fname="day$day.in"):
    """
    Read the input file and return .

    :param fname: A string name of the file to read.
    :return: .
    """
    with open(fname) as f:
        pass


if __name__ == "__main__":
    pass
EOT
chmod 755 "day$day.py"
