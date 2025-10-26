
from lark import Lark, UnexpectedInput
import os
BASE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE, "grammar.lark"), "r", encoding="utf-8") as f:
    grammar = f.read()
parser = Lark(grammar, start="start", parser="lalr", maybe_placeholders=False)

def run(name):
    p = os.path.join(BASE, "tests", "positive", name)
    with open(p, "r", encoding="utf-8") as f:
        s = f.read()
    try:
        parser.parse(s)
        print(name, "OK")
    except UnexpectedInput as e:
        print(name, "FAIL")
        print(e.get_context(s))

run("A_assignments.txt")
run("C_return_in_sub.txt")
