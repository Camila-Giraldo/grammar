#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EJEMPLO DE USO DE LA GRAMÁTICA
===============================
Este script muestra cómo usar grammar.lark para parsear código
de pseudocódigo algorítmico.
"""

from lark import Lark, UnexpectedInput
import os

# Cargar la gramática
BASE = os.path.dirname(os.path.abspath(__file__))
GRAMMAR_PATH = os.path.join(BASE, "grammar.lark")

with open(GRAMMAR_PATH, "r", encoding="utf-8") as f:
    grammar = f.read()

# Crear el parser
parser = Lark(grammar, start="start", parser="lalr")

# =============================================================================
# EJEMPLOS DE CÓDIGO VÁLIDO
# =============================================================================

print("=" * 70)
print("EJEMPLOS DE CÓDIGO VÁLIDO")
print("=" * 70)

ejemplos_validos = [
    ("Programa simple", """
BEGIN
  VAR x <- 5
  VAR y <- 10
  PRINT(x + y)
END
"""),
    
    ("Función con retorno", """
suma(a, b) BEGIN
  RETURN a + b
END

BEGIN
  PRINT(suma(3, 4))
END
"""),
    
    ("Bucle FOR", """
BEGIN
  VAR i <- 0
  FOR i <- 1 TO 10 DO
    PRINT(i)
  ENDFOR
END
"""),
    
    ("Array y condicional", """
BEGIN
  VAR arr[100]
  VAR x <- 5
  arr[1] <- 42
  
  IF (x > 0) THEN
    PRINT("Positivo")
  ELSE
    PRINT("No positivo")
  ENDIF
END
"""),
    
    ("Bucle WHILE", """
BEGIN
  VAR i <- 1
  WHILE (i <= 5) DO
    PRINT(i)
    i <- i + 1
  ENDWHILE
END
"""),
]

for nombre, codigo in ejemplos_validos:
    print(f"\n▶ {nombre}")
    try:
        tree = parser.parse(codigo)
        print("  ✓ Parseado correctamente")
    except Exception as e:
        print(f"  ✗ Error inesperado: {e}")

# =============================================================================
# EJEMPLOS DE CÓDIGO INVÁLIDO
# =============================================================================

print("\n" + "=" * 70)
print("EJEMPLOS DE CÓDIGO INVÁLIDO (deben ser rechazados)")
print("=" * 70)

ejemplos_invalidos = [
    ("Asignación a número", """
BEGIN
  3 <- x
END
"""),
    
    ("RETURN en bloque principal", """
BEGIN
  RETURN 5
END
"""),
    
    ("Asignación en argumento", """
BEGIN
  PRINT(x <- 5)
END
"""),
    
    ("Declaración sin VAR", """
BEGIN
  A[10]
END
"""),
]

for nombre, codigo in ejemplos_invalidos:
    print(f"\n▶ {nombre}")
    try:
        tree = parser.parse(codigo)
        print("  ✗ NO DEBIÓ PASAR (error en la gramática)")
    except UnexpectedInput as e:
        print("  ✓ Rechazado correctamente")
    except Exception as e:
        print(f"  ✓ Rechazado con excepción: {type(e).__name__}")

# =============================================================================
# VISUALIZAR EL ÁRBOL DE SINTAXIS
# =============================================================================

print("\n" + "=" * 70)
print("VISUALIZACIÓN DEL ÁRBOL DE SINTAXIS")
print("=" * 70)

codigo_ejemplo = """
suma(a, b) BEGIN
  RETURN a + b
END

BEGIN
  VAR x <- 5
  PRINT(suma(x, 3))
END
"""

print("\nCódigo:")
print(codigo_ejemplo)
print("\nÁrbol de sintaxis:")
tree = parser.parse(codigo_ejemplo)
print(tree.pretty())

print("\n" + "=" * 70)
print("EJEMPLO COMPLETO")
print("=" * 70)
