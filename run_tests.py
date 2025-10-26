#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os, glob
from lark import Lark, UnexpectedInput

BASE = os.path.dirname(os.path.abspath(__file__))
GRAMMAR_PATH = os.path.join(BASE, "grammar.lark")
NEG_DIR = os.path.join(BASE, "tests", "negative")
POS_DIR = os.path.join(BASE, "tests", "positive")

def load_parser():
    with open(GRAMMAR_PATH, "r", encoding="utf-8") as f:
        grammar = f.read()
    return Lark(grammar, start="start", parser="lalr", maybe_placeholders=False)

def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def run_group(parser, folder, expect_ok: bool):
    results = []
    for path in sorted(glob.glob(os.path.join(folder, "*.txt"))):
        name = os.path.basename(path)
        code = read_file(path)
        try:
            parser.parse(code)
            ok = expect_ok
            info = "OK" if ok else "DEBIÓ FALLAR"
        except UnexpectedInput as e:
            ok = not expect_ok
            snippet = e.get_context(code)
            info = ("FALLÓ" if not expect_ok else f"NO DEBÍA FALLAR\n--- Contexto ---\n{snippet}")
        except Exception as e:
            ok = False if expect_ok else True
            info = f"EXCEPCIÓN {'INDEBIDA' if expect_ok else 'ACEPTABLE'}: {e.__class__.__name__}"
        results.append((name, ok, info))
    return results

def main():
    try:
        parser = load_parser()
    except Exception as e:
        print("No se pudo crear el parser. Instala Lark con: pip install lark-parser lark")
        print("Detalle:", e)
        sys.exit(2)

    neg_results = run_group(parser, NEG_DIR, expect_ok=False)
    pos_results = run_group(parser, POS_DIR, expect_ok=True)

    total = len(neg_results) + len(pos_results)
    passed = sum(1 for _, ok, _ in neg_results + pos_results if ok)

    print("== RESULTADOS ==")
    print(f"Total: {total}  |  Pasaron: {passed}  |  Fallaron: {total - passed}")
    print("\n-- Negativos (DEBEN FALLAR) --")
    for name, ok, info in neg_results:
        print(f"[{'✓' if ok else '✗'}] {name}: {info}")
    print("\n-- Positivos (DEBEN PASAR) --")
    for name, ok, info in pos_results:
        print(f"[{'✓' if ok else '✗'}] {name}: {info}")

if __name__ == "__main__":
    main()
