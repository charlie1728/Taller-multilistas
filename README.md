# Definiciones de Node, Stack y Queue proporcionadas por el usuario
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class Stack:
    def __init__(self):
        self.top = None
        self.size = 0

    def push(self, value):
        new_node = Node(value)
        new_node.next = self.top
        self.top = new_node
        self.size += 1

    def pop(self):
        if not self.top:
            return None
        val = self.top.value
        self.top = self.top.next
        self.size -= 1
        return val

    def peek(self):
        return self.top.value if self.top else None

    def is_empty(self):
        return self.top is None
    
    def __len__(self):
        return self.size
    
class Queue:
    def __init__(self):
        self.front = None
        self.rear = None

    def enqueue(self, value):
        new_node = Node(value)
        if not self.rear:
            self.front = self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node

    def dequeue(self):
        if not self.front:
            return None
        val = self.front.value
        self.front = self.front.next
        if not self.front:
            self.rear = None
        return val

    def is_empty(self):
        return self.front is None

# --- Implementación del Ejercicio ---

def validar_balanceo_parentesis(ecuacion_str):
    """
    Paso 1: Verifica si el balanceo de los paréntesis es correcto.
    Utiliza la clase Stack.
    """
    pila = Stack()
    mapeo = {')': '(', ']': '[', '}': '{'}
    apertura = set(mapeo.values())

    for char in ecuacion_str:
        if char in apertura:
            pila.push(char)
        elif char in mapeo:
            if pila.is_empty() or pila.pop() != mapeo[char]:
                return f"Error: Paréntesis desbalanceado o tipo incorrecto. Se esperaba '{mapeo[char]}' pero se encontró '{char}'."
    
    if not pila.is_empty():
        return f"Error: Paréntesis de apertura sin cerrar. Queda un '{pila.peek()}' sin emparejar."
        
    return "OK_BALANCEO"

def identificar_errores_estructura(ecuacion_str):
    """
    Paso 2: Identifica errores de estructura matemática (operadores, variable 'x', signo '=').
    Se asume que el balanceo de paréntesis es correcto al llegar aquí.
    """
    operadores = {'+', '-', '*', '/'}
    digitos = set('0123456789.')
    
    # 1. Uso incorrecto de operadores (*, +, *, =) o falta de un único '='
    count_igual = 0
    
    # Pre-limpieza para facilitar el análisis de operadores (eliminar espacios)
    ecuacion_limpia = ecuacion_str.replace(' ', '')
    
    # Analizar Operadores
    for i, char in enumerate(ecuacion_limpia):
        if char in operadores:
            # Error: Operador al inicio (ej: +2*x) o al final (ej: 2*x+) de la expresión.
            if i == 0 or i == len(ecuacion_limpia) - 1:
                 return f"Error: Operador '{char}' en posición inválida (inicio/fin)."

            # Error: Doble operador (ej: 2**x)
            prev_char = ecuacion_limpia[i-1]
            if prev_char in operadores:
                 return f"Error: Doble operador '{prev_char}{char}'."
            
            # Error: Operador justo antes de un cierre de paréntesis (ej: (2+))
            if ecuacion_limpia[i+1] in set(')]}'):
                 return f"Error: Operador '{char}' seguido inmediatamente por un paréntesis de cierre."
            
            # Error: Operador justo después de un apertura de paréntesis (ej: (+2))
            if prev_char in set('([{'):
                 # Esto permite el signo unario: ( -2*x )
                 if char != '-' and char != '+':
                    return f"Error: Operador '{char}' inmediatamente después de un paréntesis de apertura."
        
        # Conteo del signo de igualdad
        if char == '=':
            count_igual += 1

    # Error: Falta de un único '='
    if count_igual != 1:
        return "Error: Ausencia o multiplicidad del signo '=' (Debe haber uno y solo uno)."

    # 2. Falta de la variable x (se verifica que exista al menos una 'x')
    if 'x' not in ecuacion_limpia:
        return "Error: Ausencia de la variable 'x'."

    # 3. Estructura general bien formada
    return "OK_ESTRUCTURA"


def resolver_ecuacion_primer_grado(ecuacion_str):
    """
    Paso 5: Resuelve la ecuación de primer grado y devuelve el valor de x.
    Esto requiere evaluar la expresión, simplificarla a ax + b = 0, y resolver para x.
    Usaremos la Queue para implementar el algoritmo Shunting-Yard (Infix a Postfix)
    y luego evaluaremos el Postfix.
    """
    # 1. Preparación y tokenización
    # Para el ámbito de este problema, simplificaremos asumiendo una entrada limpia
    # que solo usa paréntesis, operadores, números y 'x'.
    
    # Sustitución de paréntesis anidados por solo uno para simplificar la lógica
    ecuacion_str = ecuacion_str.replace('{', '(').replace('}', ')').replace('[', '(').replace(']', ')')
    
    tokens = []
    i = 0
    while i < len(ecuacion_str):
        char = ecuacion_str[i]
        
        if char.isspace():
            i += 1
            continue
        
        if char in '()+-*/=' or char == 'x':
            tokens.append(char)
            i += 1
        elif char.isdigit() or char == '.':
            # Leer el número completo
            num_str = ""
            while i < len(ecuacion_str) and (ecuacion_str[i].isdigit() or ecuacion_str[i] == '.'):
                num_str += ecuacion_str[i]
                i += 1
            tokens.append(num_str)
        else:
            # Ignorar otros caracteres no válidos (aunque ya deberíamos haberlos atrapado)
            i += 1

    # 2. Separación en Lado Izquierdo (LI) y Lado Derecho (LD)
    try:
        idx_igual = tokens.index('=')
        tokens_li = tokens[:idx_igual]
        tokens_ld = tokens[idx_igual+1:]
    except ValueError:
        # Esto no debería ocurrir si el paso 2 fue 'OK'
        return "Error: Signo '=' no encontrado."

    # 3. Conversión a Postfix y simplificación (Coeficientes de x y Constantes)
    
    # Precedencia de operadores
    precedencia = {'+': 1, '-': 1, '*': 2, '/': 2}
    
    def infix_to_postfix_and_simplify(exp_tokens):
        """
        Convierte Infix a Postfix (usando Shunting-Yard) y luego lo evalúa
        para obtener un par (coef_x, constante).
        """
        # Utilizaremos una pila para operadores y una cola para la salida Postfix
        pila_ops = Stack()
        cola_postfix = Queue()
        
        # Algoritmo Shunting-Yard (Infix a Postfix)
        for token in exp_tokens:
            if token.isdigit() or (token[0] in '+-' and token[1:].replace('.', '').isdigit()) or token.replace('.', '').isdigit():
                # Es un número (incluye el signo si es unario)
                cola_postfix.enqueue(float(token))
            elif token == 'x':
                cola_postfix.enqueue('x')
            elif token == '(':
                pila_ops.push(token)
            elif token == ')':
                top_token = pila_ops.pop()
                while top_token != '(':
                    if top_token is None: 
                        # Si llega aquí, es un error de balanceo (que ya se verificó)
                        break 
                    cola_postfix.enqueue(top_token)
                    top_token = pila_ops.pop()
            elif token in precedencia:
                # Es un operador
                while (not pila_ops.is_empty() and pila_ops.peek() != '(' and 
                       precedencia.get(pila_ops.peek(), 0) >= precedencia[token]):
                    cola_postfix.enqueue(pila_ops.pop())
                pila_ops.push(token)

        while not pila_ops.is_empty():
            cola_postfix.enqueue(pila_ops.pop())
            
        # Evaluación Postfix
        pila_eval = Stack()
        
        while not cola_postfix.is_empty():
            token = cola_postfix.dequeue()
            
            if isinstance(token, float):
                # Es un número: (coef_x, constante) -> (0.0, número)
                pila_eval.push((0.0, token))
            elif token == 'x':
                # Es 'x': (coef_x, constante) -> (1.0, 0.0)
                pila_eval.push((1.0, 0.0))
            elif token in operadores:
                # Es un operador, necesita dos operandos
                
                # Pop de dos tuplas: (coef_x_2, constante_2) y (coef_x_1, constante_1)
                op2 = pila_eval.pop()
                op1 = pila_eval.pop()

                if op1 is None or op2 is None:
                    # Error inesperado en la evaluación
                    return None
                    
                coef_x_1, const_1 = op1
                coef_x_2, const_2 = op2
                
                # Realizar la operación simbólica
                nuevo_coef_x = 0.0
                nueva_const = 0.0
                
                if token == '+':
                    nuevo_coef_x = coef_x_1 + coef_x_2
                    nueva_const = const_1 + const_2
                elif token == '-':
                    nuevo_coef_x = coef_x_1 - coef_x_2
                    nueva_const = const_1 - const_2
                elif token == '*':
                    # Para una ecuación de primer grado, solo permitimos:
                    # 1. Constante * Constante (que ya estaría simplificada)
                    # 2. Constante * (a*x + b) o (a*x + b) * Constante
                    # Multiplicar (ax+b) * (cx+d) resulta en x^2, lo cual no es primer grado.
                    
                    # Caso: Número * (a*x + b)
                    if coef_x_1 == 0.0: # op1 es una constante (const_1)
                        nuevo_coef_x = const_1 * coef_x_2
                        nueva_const = const_1 * const_2
                    # Caso: (a*x + b) * Número
                    elif coef_x_2 == 0.0: # op2 es una constante (const_2)
                        nuevo_coef_x = coef_x_1 * const_2
                        nueva_const = const_1 * const_2
                    else:
                        # Multiplicación de dos términos con 'x' -> x^2. ¡No es primer grado!
                        return None # Indica un error de formato/grado
                        
                elif token == '/':
                    # Para división, solo permitimos (a*x + b) / Constante
                    if coef_x_2 == 0.0: # op2 es una constante (const_2)
                        if const_2 == 0:
                            return None # División por cero
                        nuevo_coef_x = coef_x_1 / const_2
                        nueva_const = const_1 / const_2
                    else:
                        # División por término con 'x' -> ¡No es primer grado!
                        return None

                pila_eval.push((nuevo_coef_x, nueva_const))
                
        if pila_eval.is_empty() or len(pila_eval) > 1:
            return None # Error de formato Postfix

        return pila_eval.pop()


    # 4. Obtener coeficientes (ax + b) para ambos lados
    res_li = infix_to_postfix_and_simplify(tokens_li)
    res_ld = infix_to_postfix_and_simplify(tokens_ld)
    
    if res_li is None or res_ld is None:
        return "Error: Expresión no válida para una ecuación de primer grado (ej. División por cero o multiplicación de 'x')."

    # Simplificación: LI - LD = 0  => (a_li*x + b_li) - (a_ld*x + b_ld) = 0
    # => (a_li - a_ld)*x + (b_li - b_ld) = 0
    
    a_li, b_li = res_li
    a_ld, b_ld = res_ld
    
    a = a_li - a_ld # Coeficiente final de x
    b = b_li - b_ld # Constante final
    
    # 5. Resolver ax + b = 0
    
    if abs(a) < 1e-9: # 'a' es efectivamente cero (ej. 0.000000001)
        if abs(b) < 1e-9:
            # 0*x + 0 = 0 -> Infinitas soluciones
            return "Error: Infinitas soluciones (0=0)."
        else:
            # 0*x + b = 0 (donde b != 0) -> No hay solución
            return "Error: Sin solución (contradicción)."
    else:
        # a*x + b = 0 => x = -b / a
        x = -b / a
        # Devolver con precisión de tres decimales
        return f"{x:.3f}"


def procesar_ecuacion(ecuacion):
    """
    Función principal que sigue los pasos 1 al 5.
    """
    
    # Paso 1: Balanceo de paréntesis
    resultado_balanceo = validar_balanceo_parentesis(ecuacion)
    if resultado_balanceo != "OK_BALANCEO":
        # Devuelve el primer error encontrado (Punto 4)
        return resultado_balanceo

    # Paso 2 y 3: Identificar errores de estructura
    resultado_estructura = identificar_errores_estructura(ecuacion)
    
    if resultado_estructura != "OK_ESTRUCTURA":
        # Devuelve el primer error encontrado (Punto 4)
        return resultado_estructura
    
    # Si todo es OK_ESTRUCTURA (Punto 3)
    # Nota: El ejercicio pide devolver "OK" si está bien estructurada,
    # y luego, si es una ecuación (que ya se verificó con el '='), pide resolverla.
    # La solución de la ecuación es el resultado final.
    # Si la estructura es correcta, procedemos a resolver.
    
    # Paso 5: Resolver la ecuación
    resultado_final = resolver_ecuacion_primer_grado(ecuacion)
    
    # Si la resolución devuelve un error, se interpreta como el primer error encontrado (Punto 4)
    if resultado_final.startswith("Error:"):
        return resultado_final
    elif resultado_final.startswith("OK_ESTRUCTURA"):
        # Esto no debería pasar en la lógica actual, pero por si acaso.
        return "OK"
    else:
        # Es la solución de 'x' con 3 decimales
        return resultado_final

# --- Ejemplos de Uso ---

ecuaciones = [
    "{2*x + 3} - x - 1] = (5 + x)", # Mal balanceo (cierre ']' en lugar de '}')
    "2x + 3 - x = 5 + x",           # Ausencia de paréntesis (pero bien balanceada, NO)
    "((x + 1) * 2) = 10",           # OK
    "x + 5 = 10",                   # OK (ejemplo simple sin anidación)
    "2*x - 4 = 2 * (x - 2)",        # Infinitas soluciones (2x - 4 = 2x - 4 -> 0=0)
    "3*x + 1 = 3 * x - 2",          # Sin solución (3x + 1 = 3x - 2 -> 3=0)
    "2 * x + 3 * )",                # Operador antes de cierre
    "2 + + x = 5",                  # Doble operador
    "2 * (1 + 2) + 3",              # Falta de '='
    "2 + 3 = 5",                    # Falta de 'x'
    "2 * (x + 1) / 0 = 10",         # División por cero
    "2 * (x + 1) * (x + 2) = 0"     # No es primer grado
]

print("--- Procesando Ecuaciones ---")
for i, eq in enumerate(ecuaciones):
    print(f"\n[{i+1}] Entrada: {eq}")
    resultado = procesar_ecuacion(eq)
    print(f"    Resultado: {resultado}")
    print("-" * 20)

# El ejemplo de la imagen:
ecuacion_ejemplo = "{2*x + 3} - x - 1] = (5 + x)"
print(f"\n[Imagen] Entrada: {ecuacion_ejemplo}")
resultado_ejemplo = procesar_ecuacion(ecuacion_ejemplo)
print(f"    Resultado: {resultado_ejemplo}")
