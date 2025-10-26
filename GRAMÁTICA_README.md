# Gramática de Pseudocódigo Algorítmico

## 📋 Descripción

Este proyecto contiene una gramática completa para un lenguaje de pseudocódigo algorítmico, implementada usando [Lark](https://github.com/lark-parser/lark) (un parser moderno para Python).

## 🎯 Características del Lenguaje

### Estructuras de datos
- ✅ Variables simples con inicialización: `VAR x <- 5`
- ✅ Arrays unidimensionales y multidimensionales: `VAR arr[100]`, `VAR matriz[10][20]`
- ✅ Objetos y clases: `OBJ miObjeto MiClase`
- ✅ Acceso a atributos: `objeto.campo`
- ✅ Segmentos de arrays: `arr[1..10]`

### Estructuras de control
- ✅ Condicional: `IF (condición) THEN ... ELSE ... ENDIF`
- ✅ Bucle mientras: `WHILE (condición) DO ... ENDWHILE`
- ✅ Bucle para: `FOR i <- 1 TO 10 DO ... ENDFOR`
- ✅ Bucle repetir-hasta: `REPEAT ... UNTIL (condición)`

### Expresiones
- ✅ Aritméticas: `+`, `-`, `*`, `/`, `mod`, `^` (potencia)
- ✅ Lógicas: `AND`, `OR`, `NOT`
- ✅ Relacionales: `=`, `<>`, `!=`, `<`, `>`, `<=`, `>=`, `≤`, `≥`
- ✅ Literales: números, strings, booleanos (`True`, `False`), `null`
- ✅ Operadores especiales: `⌊x⌋` (piso), `⌈x⌉` (techo)

### Funciones y subrutinas
- ✅ Definición de funciones con parámetros
- ✅ Llamadas a función: `CALL func(args)` o `func(args)`
- ✅ Retorno de valores: `RETURN expresión`
- ✅ Parámetros por valor, arrays y objetos

### Otras características
- ✅ Impresión: `PRINT(expresión1, expresión2, ...)`
- ✅ Comentarios: líneas que empiezan con `►`
- ✅ Operador de asignación flexible: `←`, `🡨`, o `<-`

## 🔍 Diferenciación de Contextos

Una característica importante de esta gramática es la **separación de contextos**:

### Contexto Principal (`_main`)
- Código dentro del bloque `BEGIN...END` principal
- **NO permite** usar `RETURN`
- Representa el punto de entrada del programa

### Contexto de Subrutina (`_sub`)
- Código dentro de funciones/subrutinas
- **SÍ permite** usar `RETURN`
- Representa funciones que pueden devolver valores

Esta separación previene errores como intentar hacer `RETURN` desde el programa principal.

## 📂 Estructura del Proyecto

```
grammar_runner/
├── grammar.lark          ← Gramática DOCUMENTADA (léeme aquí)
├── run_tests.py          ← Script para ejecutar todas las pruebas
├── debug_parse.py        ← Script para debug rápido
├── tests/
│   ├── positive/         ← Programas que DEBEN parsearse correctamente
│   └── negative/         ← Programas que DEBEN ser rechazados
```

## 🚀 Cómo Usar

### 1. Requisitos
```bash
pip install lark-parser
```

### 2. Ejecutar todas las pruebas
```bash
python3 run_tests.py
```

Esto verificará que:
- ✅ Todos los archivos en `tests/positive/` se parsean correctamente
- ✅ Todos los archivos en `tests/negative/` son rechazados (sintaxis inválida)

### 3. Probar un archivo específico
```bash
python3 debug_parse.py
```

### 4. Usar la gramática en tu código Python

```python
from lark import Lark

# Cargar la gramática
with open("grammar.lark", "r", encoding="utf-8") as f:
    grammar = f.read()

# Crear el parser
parser = Lark(grammar, start="start", parser="lalr")

# Parsear código
code = """
BEGIN
  VAR x <- 5
  PRINT(x)
END
"""

try:
    tree = parser.parse(code)
    print("✓ Código válido")
    print(tree.pretty())  # Ver el árbol de sintaxis
except Exception as e:
    print("✗ Error de sintaxis:", e)
```

## 📖 Ejemplos de Código Válido

### Programa simple
```
BEGIN
  VAR x <- 5
  VAR y <- 10
  PRINT(x + y)
END
```

### Función con retorno
```
suma(a, b) BEGIN
  RETURN a + b
END

BEGIN
  PRINT(suma(3, 4))
END
```

### Bucle FOR
```
BEGIN
  VAR i <- 0
  FOR i <- 1 TO 10 DO
    PRINT(i)
  ENDFOR
END
```

### Array y condicional
```
BEGIN
  VAR arr[100]
  VAR i <- 0
  
  FOR i <- 1 TO 10 DO
    arr[i] <- i * i
  ENDFOR
  
  IF (arr[5] > 20) THEN
    PRINT("arr[5] es mayor que 20")
  ELSE
    PRINT("arr[5] es menor o igual a 20")
  ENDIF
END
```

### Algoritmo completo (Floyd-Warshall)
```
Floyd(G[10000], n) BEGIN
  VAR i <- 1
  VAR j <- 1
  VAR k <- 1
  
  FOR k <- 1 TO n DO
    FOR i <- 1 TO n DO
      FOR j <- 1 TO n DO
        IF (G[(i-1)*n + k] + G[(k-1)*n + j] < G[(i-1)*n + j]) THEN
          G[(i-1)*n + j] <- G[(i-1)*n + k] + G[(k-1)*n + j]
        ENDIF
      ENDFOR
    ENDFOR
  ENDFOR
END

BEGIN
  VAR G[10000]
  VAR n <- 4
  CALL Floyd(G, n)
END
```

## 🔧 Precedencia de Operadores

### Operadores Aritméticos (de menor a mayor precedencia)
1. Suma y resta: `+`, `-`
2. Multiplicación, división, módulo: `*`, `/`, `mod`
3. Potencia: `^`, `**`

### Operadores Lógicos (de menor a mayor precedencia)
1. OR: `OR`
2. AND: `AND`
3. NOT: `NOT`

### Asociatividad
- **Izquierda**: `+`, `-`, `*`, `/`, `mod`, `AND`, `OR`
- **Derecha**: `^`, `**`, `NOT`

## ⚠️ Restricciones Importantes

### ❌ No permitido en argumentos de función
```
PRINT(x <- 5)  ← Error: asignación en argumento
```

### ❌ No permitido en condiciones
```
IF (x <- 5) THEN  ← Error: asignación en condición
  ...
ENDIF
```

### ❌ No permitido en bloque principal
```
BEGIN
  RETURN 5  ← Error: RETURN solo en funciones
END
```

### ❌ Lvalues inválidos
```
3 <- x          ← Error: número como lvalue
(a + b) <- 5    ← Error: expresión como lvalue
func() <- 10    ← Error: llamada a función como lvalue
```

## ✅ Pruebas Incluidas

El proyecto incluye 28 archivos de prueba:

**Pruebas Positivas (13)**: Programas válidos que deben parsearse correctamente
- Asignaciones básicas
- Llamadas a función
- Estructuras de control
- Algoritmos completos (Floyd-Warshall, QuickSort, etc.)

**Pruebas Negativas (15)**: Programas inválidos que deben ser rechazados
- Lvalues inválidos
- Asignaciones en contextos prohibidos
- RETURN en bloque principal
- Expresiones como statements

## 🎓 Entendiendo la Gramática

El archivo `grammar.lark` está organizado en secciones claras:

1. **Tokens**: Definición de palabras clave y símbolos
2. **Estructura del programa**: Regla principal y bloques
3. **Declaraciones**: Variables, arrays, objetos
4. **Statements**: Instrucciones ejecutables
5. **Estructuras de control**: IF, WHILE, FOR, REPEAT
6. **Expresiones**: Aritméticas, lógicas, comparaciones

## 📚 Recursos Adicionales

- [Documentación de Lark](https://lark-parser.readthedocs.io/)
- [Tutorial de gramáticas en Lark](https://lark-parser.readthedocs.io/en/latest/grammar.html)
- [EBNF (Extended Backus-Naur Form)](https://en.wikipedia.org/wiki/Extended_Backus%E2%80%93Naur_form)
