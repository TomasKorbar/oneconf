#!/usr/bin/python3
import re
import sys

if __name__ == "__main__":
    old_pylint_output_path = sys.argv[1]
    new_pylint_output_path = sys.argv[2]

    with open(old_pylint_output_path, "r") as f:
        old_pylint = f.read()

    with open(new_pylint_output_path, "r") as f:
        new_pylint = f.read()

    old_pylint_regex = re.escape(old_pylint)
    old_pylint_regex = re.sub(r":[0-9]*:",r":[0-9]*:", old_pylint_regex)

    # check if both outputs are identical except line numbers because these
    # can change on any change of code and it does not mean any problem
    if re.fullmatch(old_pylint_regex, new_pylint):
        sys.exit(0)
    else:
        # check count of problems because if a problem has been solved then
        # there is no point use in reporting failure
        old_number = len(re.findall(r"\[[R,C,W,E]0.*\]", old_pylint))
        new_number = len(re.findall(r"\[[R,C,W,E]0.*\]", new_pylint))
        if old_number > new_number:
            sys.exit(0)
        else:
            sys.exit(1)
