
from lark import Lark, UnexpectedInput
import os
BASE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE, "grammar.lark"), "r", encoding="utf-8") as f:
    grammar = f.read()
parser = Lark(grammar, start="start", parser="lalr", maybe_placeholders=False)

s = "BEGIN\n  VAR n <- 3\nEND\n"
try:
    parser.parse(s)
    print("Parsed OK")
except Exception as e:
    print("Exception:", type(e).__name__, str(e))
    if isinstance(e, UnexpectedInput):
        print("Expected:", e.expected)
        print(e.get_context(s))
