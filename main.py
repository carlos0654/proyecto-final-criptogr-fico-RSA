import tkinter as tk
from tkinter import ttk

#==============================================================================================================================
#CARLOS ANDRES DE LEON RODRIGUEZ 251630
#ALEXANDER CARRERA 25178
#==============================================================================================================================

#lista de los primeros numeros primos del 1 al 100 para agilisar el programa
PRIMOS_CONOCIDOS = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]


#
#ALGORITMOS
#
def es_primo(numero):
    #Devuelve True si "numero" es primo y False si no

    #Si es menor que dos devuelve false
    if numero < 2:
        return False

    #Si esta en la lista de primos conocidos devuelve true
    if numero in PRIMOS_CONOCIDOS:
        return True

    #Si es dividido por algun primo ya conocido devuelve false
    for primo in PRIMOS_CONOCIDOS:
        if numero % primo == 0:
            return False

    #se revisan los divisores impares desde 97 en adelante hasta la raiz de "numero"
    divisor = 97
    while divisor * divisor <= numero:
        if numero % divisor == 0:
            return False
        divisor = divisor + 2

    PRIMOS_CONOCIDOS.append(numero)   #lo agregamos como una mausquerramienta que nos servira mas tarde xdddddddddd
    return True


def mcd(a, b):
    #Maximo comun divisor con el algoritmo del pana Euclides.

    #Se repite hasta que "b" sea 0 y de alli devuelve "a"
    while b != 0:
        a, b = b, a % b
    return a


def inverso_modular(a, modulo):
    #Inverso de "a" modulo "modulo" con el algoritmo extendido del ya tu sabe (Euclides)

    residuo_anterior, residuo_actual = modulo, a % modulo
    coef_anterior, coef_actual = 0, 1
    #continua mientras el residuo no sea 0
    while residuo_actual != 0:
        cociente = residuo_anterior // residuo_actual

        residuo_anterior, residuo_actual = (
            residuo_actual,
            residuo_anterior - cociente * residuo_actual,
        )
        coef_anterior, coef_actual = (
            coef_actual,
            coef_anterior - cociente * coef_actual,
        )

    if residuo_anterior != 1:
        return None                      #no existe inverso
    #Devuelve x tal que (a * x) mod modulo = 1 con x siendo menor a 0 pero mayor a "modulo"
    return coef_anterior % modulo        #el % deja el resultado entre 0 y modulo-1


def exponenciacion_modular(base, exponente, modulo):
    #Calcular (base ** exponente) mod "modulo" sin construir la potencia completa metodo de (elevar al cuadrado y multiplicar)
    #se recorre el exponente en binario y en cada paso se reduce mod "modulo"

    resultado = 1
    base = base % modulo

    while exponente > 0:
        if exponente % 2 == 1:                    #el bit actual del exponente es 1
            resultado = (resultado * base) % modulo
        exponente = exponente // 2                #se pasa al siguiente bit
        base = (base * base) % modulo             #se aumenta la base

    return resultado


N_MINIMO = 126126        # n debe ser MAYOR que este valor
N_MAXIMO = 1000000       # n debe ser MENOR que este valor
ASCII_MIN = 32           # primer caracter imprimible (espacio)
ASCII_MAX = 126          # ultimo caracter imprimible (~)
MAX_DIGITOS = 18         # tope de digitos al leer enteros (evita numeros absurdos)

#
#ERRORES PERSONALISADOS 
# 
class ErrorRSA(Exception):
    """Error de validacion. Su texto se muestra al usuario en la interfaz."""


def solo_digitos(texto):
    #devuelve True si el texto es no vacio y todos sus caracteres son 0-9 (ASCII)
    if texto == "":
        return False
    for caracter in texto:
        if caracter not in "0123456789":
            return False
    return True


def leer_entero(texto, nombre):
    #Convierte el texto de una casilla en un entero positivo o lanza ErrorRSA
    texto = texto.strip()
    if texto == "":
        #TEST ERROR RSA
        raise ErrorRSA(f"{nombre} esta vacio. Debe ingresar un numero entero")
    if not solo_digitos(texto):
        raise ErrorRSA(f"{nombre} debe ser un entero positivo (solo digitos 0-9)" f"Se recibio: '{texto}'.")
    if len(texto) > MAX_DIGITOS:
        raise ErrorRSA(f"{nombre} es demasiado grande (maximo {MAX_DIGITOS} digitos)")
    return int(texto)


def validar_parametros(texto_p, texto_q, texto_e):
    #comprueba que p y q sean enteros primos y distintos entre 
    #ademas n tiene que estar entre 126126 < n < 1000000, e > 1 y MCD(e, φ) = 1


    #p q y e deben ser enteros
    p = leer_entero(texto_p, "p")
    q = leer_entero(texto_q, "q")
    e = leer_entero(texto_e, "e")

    #p y q deben ser primos y menores a 1,000,000
    if p >= N_MAXIMO or q >= N_MAXIMO:
        raise ErrorRSA(f"p y q deben ser menores que {N_MAXIMO}, "
                       f"porque se exige n = p·q < {N_MAXIMO}")
    if not es_primo(p):
        raise ErrorRSA(f"p = {p} no es primo.")
    if not es_primo(q):
        raise ErrorRSA(f"q = {q} no es primo.")
    if p == q:
        raise ErrorRSA(f"p y q deben ser primos distintos (ambos valen {p}).")
    
    #n dentro del rango
    n = p * q
    if not (N_MINIMO < n < N_MAXIMO):
        raise ErrorRSA(f"n = p·q = {p}·{q} = {n} esta fuera de rango: "
                       f"debe cumplirse {N_MINIMO} < n < {N_MAXIMO}.")


    phi = (p - 1) * (q - 1)
    if e <= 1:
        raise ErrorRSA(f"e = {e} no es valido: debe cumplirse e > 1.")
    divisor_comun = mcd(e, phi)
    if divisor_comun != 1:
        raise ErrorRSA(f"e = {e} no es valido: MCD(e, φ) = MCD({e}, {phi}) = "
                       f"{divisor_comun}, pero debe ser 1.")

    return {"p": p, "q": q, "n": n, "phi": phi, "e": e}


def validar_mensaje(mensaje):
    #reglas del ASCII
    if len(mensaje) == 0:
        raise ErrorRSA("El mensaje esta vacio. Escriba al menos un caracter.")

    for posicion, caracter in enumerate(mensaje, start=1):
        codigo = ord(caracter)
        if codigo < ASCII_MIN or codigo > ASCII_MAX:
            raise ErrorRSA(
                f"Caracter no admitido en la posicion {posicion}: {caracter!r} "
                f"(codigo {codigo}). Solo se permite ASCII imprimible "
                f"({ASCII_MIN} a {ASCII_MAX}): letras sin tildes, numeros, signos y espacios. "
                f"No se reemplaza nada automaticamente; corrija el mensaje.")


def cifrar_mensaje(mensaje, texto_p, texto_q, texto_e):
    parametros = validar_parametros(texto_p, texto_q, texto_e)
    validar_mensaje(mensaje)

    n = parametros["n"]
    e = parametros["e"]

    
    longitud = len(mensaje)                       #L---------------------fghdxgfyhfg
    hay_relleno = (longitud % 2 == 1)
    mensaje_completo = mensaje + " " if hay_relleno else mensaje

    filas = []
    bloques_cifrados = []
    for indice in range(0, len(mensaje_completo), 2):
        caracter1 = mensaje_completo[indice]
        caracter2 = mensaje_completo[indice + 1]
        codigo1 = ord(caracter1)
        codigo2 = ord(caracter2)

        m = codigo1 * 1000 + codigo2
        c = exponenciacion_modular(m, e, n)

        es_relleno = hay_relleno and indice + 2 == len(mensaje_completo)
        caracteres_txt = f"'{caracter1}' '{caracter2}'" + (" (relleno)" if es_relleno else "")

        filas.append({"numero": indice // 2 + 1, "caracteres_txt": caracteres_txt,
                      "codigo1": codigo1, "codigo2": codigo2, "m": m, "c": c})

        
        bloques_cifrados.append(f"{c:06d}")

    texto_cifrado = " ".join(bloques_cifrados)    #bloques separados por espacio


    return {"parametros": parametros, "texto_cifrado": texto_cifrado,
            "longitud": longitud, "hay_relleno": hay_relleno,
            "filas": filas}





#
#Interface Grafica
#

COLOR_ERROR = "#b00020"
def crear_campos_rsa(padre, fila):
    """Crea las casillas p, q y e en una fila. Devuelve sus tres StringVar."""
    var_p, var_q, var_e = tk.StringVar(), tk.StringVar(), tk.StringVar()
    marco = ttk.Frame(padre)
    marco.grid(row=fila, column=0, columnspan=2, sticky="w", pady=4)
    for etiqueta, variable in (("p:", var_p), ("q:", var_q), ("e:", var_e)):
        ttk.Label(marco, text=etiqueta).pack(side="left", padx=(0, 3))
        ttk.Entry(marco, textvariable=variable, width=12).pack(side="left", padx=(0, 14))
    return var_p, var_q, var_e


def crear_texto_solo_lectura(padre, alto):
    """Cuadro de texto con barra de desplazamiento que el usuario no puede editar.
    Devuelve (marco, widget_texto)."""
    marco = ttk.Frame(padre)
    texto = tk.Text(marco, height=alto, wrap="word", font="TkFixedFont", state="disabled")
    barra = ttk.Scrollbar(marco, orient="vertical", command=texto.yview)
    texto.configure(yscrollcommand=barra.set)
    texto.pack(side="left", fill="both", expand=True)
    barra.pack(side="right", fill="y")
    return marco, texto


def escribir_texto(texto_widget, contenido):
    """Reemplaza el contenido de un Text de solo lectura."""
    texto_widget.configure(state="normal")
    texto_widget.delete("1.0", "end")
    texto_widget.insert("1.0", contenido)
    texto_widget.configure(state="disabled")


def crear_fila_datos(padre, fila, datos):
    """Fila de datos de solo lectura. 'datos' = lista de (etiqueta, StringVar, ancho)."""
    marco = ttk.Frame(padre)
    marco.grid(row=fila, column=0, columnspan=3, sticky="w", pady=2)
    for etiqueta, variable, ancho in datos:
        ttk.Label(marco, text=etiqueta).pack(side="left", padx=(0, 3))
        ttk.Entry(marco, textvariable=variable, width=ancho, state="readonly").pack(side="left", padx=(0, 14))


def crear_tabla(padre, columnas):
    marco = ttk.Frame(padre)
    marco.rowconfigure(0, weight=1)
    marco.columnconfigure(0, weight=1)

    ids = [f"col{i}" for i in range(len(columnas))]

    tabla = ttk.Treeview(
        marco,
        columns=ids,
        show="headings",
        height=6
    )

    for identificador, (titulo, ancho) in zip(ids, columnas):
        tabla.heading(identificador, text=titulo)
        tabla.column(
            identificador,
            width=ancho,
            minwidth=ancho,
            stretch=False,
            anchor="center"
        )

    barra_vertical = ttk.Scrollbar(
        marco,
        orient="vertical",
        command=tabla.yview
    )

    barra_horizontal = ttk.Scrollbar(
        marco,
        orient="horizontal",
        command=tabla.xview
    )

    tabla.configure(
        yscrollcommand=barra_vertical.set,
        xscrollcommand=barra_horizontal.set
    )

    tabla.grid(row=0, column=0, sticky="nsew")
    barra_vertical.grid(row=0, column=1, sticky="ns")
    barra_horizontal.grid(row=1, column=0, sticky="ew")

    return marco, tabla


def llenar_tabla(tabla, filas):
    """Borra la tabla y la llena con 'filas' (lista de tuplas)."""
    tabla.delete(*tabla.get_children())
    for valores in filas:
        tabla.insert("", "end", values=valores)


def crear_zona_detalle(padre, columnas):
    marco, tabla = crear_tabla(padre, columnas)
    marco.pack(fill="both", expand=True, pady=(8, 0))
    return tabla

def evitar_tabulador(texto_widget):
    """En un Text, la tecla Tab insertaria un tabulador (caracter no admitido).
    Se cambia para que Tab / Shift+Tab muevan el foco entre casillas."""
    texto_widget.bind("<Tab>", lambda evento: (evento.widget.tk_focusNext().focus(), "break")[1])
    texto_widget.bind("<Shift-Tab>", lambda evento: (evento.widget.tk_focusPrev().focus(), "break")[1])


def copiar_al_portapapeles(ventana, contenido):
    ventana.clipboard_clear()
    ventana.clipboard_append(contenido)


#PESTAÑA DECIFRAR
#HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
def crear_pestana_cifrar(cuaderno, al_enviar_a_descifrar):

    pestana = ttk.Frame(cuaderno, padding=10)

    ultimo_resultado = None

    # VARIABLES
    var_longitud = tk.StringVar()
    var_relleno = tk.StringVar()
    var_llave = tk.StringVar()
    var_n = tk.StringVar()
    var_phi = tk.StringVar()

    def cifrar():
        nonlocal ultimo_resultado

        limpiar_resultados()

        mensaje = txt_mensaje.get("1.0", "end-1c")

        try:
            resultado = cifrar_mensaje(
                mensaje,
                var_p.get(),
                var_q.get(),
                var_e.get()
            )

        except ErrorRSA as error:
            lbl_error.configure(text="⚠ " + str(error))
            return

        except Exception as error:
            lbl_error.configure(text=f"⚠ Error inesperado: {error}")
            return

        lbl_error.configure(text="")

        ultimo_resultado = resultado
        mostrar_resultado(resultado)


    def mostrar_resultado(resultado):

        parametros = resultado["parametros"]

        n = parametros["n"]
        phi = parametros["phi"]
        e = parametros["e"]

        escribir_texto(txt_cifrado, resultado["texto_cifrado"])

        var_longitud.set(str(resultado["longitud"]))

        var_relleno.set(
            "Si (se agrego 1 espacio al final)"
            if resultado["hay_relleno"] else "No"
        )

        var_llave.set(f"({e}, {n})")
        var_n.set(str(n))
        var_phi.set(str(phi))

        filas_tabla = []

        for fila in resultado["filas"]:
            filas_tabla.append((
                fila["numero"],
                fila["caracteres_txt"],
                f"{fila['codigo1']:03d} {fila['codigo2']:03d}",
                f"{fila['m']:06d}",
                f"{fila['m']}^{e} mod {n} = {fila['c']}",
                f"{fila['c']:06d}"
            ))


        llenar_tabla(tabla, filas_tabla)


        btn_enviar.configure(state="normal")

    def copiar_c():
        if ultimo_resultado is not None:
            copiar_al_portapapeles(
                pestana,
                ultimo_resultado["texto_cifrado"]
            )


    def enviar():
        """Envia el resultado a la pestaña Descifrar."""

        if ultimo_resultado is None:
            return

        parametros = ultimo_resultado["parametros"]

        al_enviar_a_descifrar(
            ultimo_resultado["texto_cifrado"],
            ultimo_resultado["longitud"],
            parametros["p"],
            parametros["q"],
            parametros["e"]
        )


    def limpiar_resultados():
        nonlocal ultimo_resultado

        ultimo_resultado = None

        escribir_texto(txt_cifrado, "")

        llenar_tabla(tabla, [])

        for variable in (
            var_longitud,
            var_relleno,
            var_llave,
            var_n,
            var_phi
        ):
            variable.set("")

        btn_enviar.configure(state="disabled")


    def limpiar_todo():

        limpiar_resultados()

        lbl_error.configure(text="")

        txt_mensaje.delete("1.0", "end")

        for variable in (var_p, var_q, var_e):
            variable.set("")


    #Interface grafica
    marco = ttk.LabelFrame(pestana, text="Entradas", padding=8)
    marco.pack(fill="x")
    marco.columnconfigure(1, weight=1)

    ttk.Label(
        marco,
        text="Mensaje a cifrar:"
    ).grid(row=0, column=0, sticky="nw", padx=(0, 6))

    txt_mensaje = tk.Text(marco, height=3, wrap="word")
    txt_mensaje.grid(row=0, column=1, sticky="ew", pady=2)

    evitar_tabulador(txt_mensaje)

    var_p, var_q, var_e = crear_campos_rsa(marco, fila=1)

    botones = ttk.Frame(marco)
    botones.grid(row=2, column=0, columnspan=2, sticky="w", pady=(4, 0))

    ttk.Button(
        botones,
        text="Cifrar",
        command=lambda: cifrar()
    ).pack(side="left", padx=(0, 6))

    ttk.Button(
        botones,
        text="Limpiar",
        command=lambda: limpiar_todo()
    ).pack(side="left")

    lbl_error = ttk.Label(
        pestana,
        text="",
        foreground=COLOR_ERROR,
        wraplength=1000,
        justify="left"
    )

    lbl_error.pack(fill="x", pady=4)


    marco_resultados = ttk.LabelFrame(
        pestana,
        text="Resultados",
        padding=8
    )

    marco_resultados.pack(fill="x")
    marco_resultados.columnconfigure(1, weight=1)

    ttk.Label(
        marco_resultados,
        text="Texto cifrado C:"
    ).grid(row=0, column=0, sticky="nw", padx=(0, 6))

    marco_c, txt_cifrado = crear_texto_solo_lectura(
        marco_resultados,
        3
    )

    marco_c.grid(row=0, column=1, sticky="ew", pady=2)

    botones_resultado = ttk.Frame(marco_resultados)
    botones_resultado.grid(row=0, column=2, sticky="n", padx=(6, 0))

    ttk.Button(
        botones_resultado,
        text="Copiar C",
        command=lambda: copiar_c()
    ).pack(fill="x", pady=1)

    btn_enviar = ttk.Button(
        botones_resultado,
        text="Enviar a Descifrar",
        command=lambda: enviar(),
        state="disabled"
    )

    btn_enviar.pack(fill="x", pady=1)






    crear_fila_datos(marco_resultados, 1, [
        ("Longitud original L:", var_longitud, 8),
        ("Relleno:", var_relleno, 34)
    ])

    crear_fila_datos(marco_resultados, 2, [
        ("Llave publica (e, n):", var_llave, 20),
        ("n:", var_n, 10),
        ("φ:", var_phi, 10)
    ])


    tabla = crear_zona_detalle(pestana, [
        ("N.º", 45),
        ("Caracteres", 130),
        ("ASCII", 100),
        ("Bloque m", 100),
        ("Calculo", 230),
        ("Bloque c", 100)
    ])
    # DEVOLVER LA PESTAÑA
    return pestana




def descifrar_mensaje(texto_cifrado, texto_longitud, texto_p, texto_q, texto_e):
        #devuelve parametros d mensaje longitud hay_relleno filas


        parametros = validar_parametros(texto_p, texto_q, texto_e)
        n = parametros["n"]
        phi = parametros["phi"]
        e = parametros["e"]

        longitud = leer_entero(texto_longitud, "L")

        bloques_texto = texto_cifrado.split()#separa por espacios
        if len(bloques_texto) == 0:
            raise ErrorRSA("El texto cifrado C esta vacio")

        valores_c = []
        for numero, bloque in enumerate(bloques_texto, start=1):
            if len(bloque) != 6 or not solo_digitos(bloque):
                raise ErrorRSA(f"El bloque #{numero} ('{bloque}') esta mal formado: cada bloque " f"debe tener exactamente 6 digitos")
            c = int(bloque)
            if c >= n:
                raise ErrorRSA(
                    f"El bloque #{numero} ({bloque}) esta fuera de rango: "
                    f"debe cumplirse 0 <= c < n = {n}."
                )
            valores_c.append(c)

        #Revisar que L
        k = len(valores_c)
        if longitud != 2 * k and longitud != 2 * k - 1:
            raise ErrorRSA(f"L = {longitud} no es coherente")
        hay_relleno = (longitud == 2 * k - 1)

        d = inverso_modular(e, phi)
  
        filas = []
        mensaje_completo = ""
        for numero, c in enumerate(valores_c, start=1):
            m = exponenciacion_modular(c, d, n)
            codigo1 = m // 1000
            codigo2 = m % 1000

            for codigo in (codigo1, codigo2):
                if codigo < ASCII_MIN or codigo > ASCII_MAX:
                    raise ErrorRSA( f"revise que c, p, q y e correspondan correctamente")

            caracter1 = chr(codigo1)
            caracter2 = chr(codigo2)
            mensaje_completo = mensaje_completo + caracter1 + caracter2

            es_relleno = hay_relleno and numero == k
            caracteres_txt = f"'{caracter1}' '{caracter2}'" + (" (relleno)" if es_relleno else "")
            filas.append({"numero": numero, "c": c, "m": m, "codigo1": codigo1, "codigo2": codigo2, "caracteres_txt": caracteres_txt})

        if hay_relleno:
            ultimo = mensaje_completo[-1]
            if ultimo != " ":
                raise ErrorRSA(f"L indica que hubo relleno, pero el ultimo caracter recuperado " f"es {ultimo!r} y deberia ser un espacio")
            mensaje = mensaje_completo[:-1]
        else:
            mensaje = mensaje_completo

        return {"parametros": parametros, "d": d, "mensaje": mensaje,
                "longitud": longitud, "hay_relleno": hay_relleno,
                "filas": filas}


#PESTAÑA DECIFRAR
#HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
def crear_pestaña_descifrar(cuaderno):

    pestaña = ttk.Frame(cuaderno, padding=11)

    ultimo_resultado = None

    # VARIABLES
    var_longitud_entrada = tk.StringVar()
    var_d = tk.StringVar()
    var_n = tk.StringVar()
    var_phi = tk.StringVar()
    var_p = tk.StringVar()
    var_q = tk.StringVar()
    var_e = tk.StringVar()
    var_longitud = tk.StringVar()
    var_relleno = tk.StringVar()
    var_mensaje_comillas = tk.StringVar()

    marco = ttk.LabelFrame(pestaña, text="Entradas", padding=8)
    marco.pack(fill="x")
    marco.columnconfigure(1, weight=1)

    #COMPONENTES ----------------------------------------
    ttk.Label(marco, text="Texto cifrado C:").grid(
        row=0, column=0, sticky="nw", padx=(0, 6)
    )

    txt_cifrado = tk.Text(marco, height=3, wrap="word")
    txt_cifrado.grid(row=0, column=1, sticky="ew", pady=2)
    evitar_tabulador(txt_cifrado)

    fila_l = ttk.Frame(marco)
    fila_l.grid(row=1, column=0, columnspan=2, sticky="w", pady=4)

    ttk.Label(fila_l, text="Longitud original L:").pack(side="left", padx=(0, 3))
    ttk.Entry(fila_l, textvariable=var_longitud_entrada, width=8).pack(side="left")

    var_p, var_q, var_e = crear_campos_rsa(marco, fila=2)





    botones = ttk.Frame(marco)
    botones.grid(row=3, column=0, columnspan=2, sticky="w", pady=(4, 0))
    ttk.Button(botones, text="Limpiar", command=lambda: limpiar_todo()).pack(side="left")
    
    lbl_error = ttk.Label(
        pestaña, text="", foreground=COLOR_ERROR,
        wraplength=1000, justify="left"
    )

    lbl_error.pack(fill="x", pady=4)
    marco_resultados = ttk.LabelFrame(
        pestaña, text="Resultados", padding=8
    )
    marco_resultados.pack(fill="x")
    marco_resultados.columnconfigure(1, weight=1)
    crear_fila_datos(marco_resultados, 0, [
        ("Exponente privado d:", var_d, 10),
        ("n:", var_n, 10),
        ("φ:", var_phi, 10)
    ])

    crear_fila_datos(marco_resultados, 1, [
        ("Longitud original L:", var_longitud, 8),
        ("Relleno:", var_relleno, 40)
    ])

    ttk.Label(marco_resultados, text="Mensaje recuperado:").grid(
        row=2, column=0, sticky="nw", padx=(0, 6)
    )

    marco_mensaje, txt_mensaje = crear_texto_solo_lectura(
        marco_resultados, 3
    )
    marco_mensaje.grid(row=2, column=1, sticky="ew", pady=2)

    ttk.Button(
        marco_resultados,
        text="Copiar mensaje",
        command=lambda: copiar_mensaje()
    ).grid(row=2, column=2, sticky="n", padx=(6, 0))
    ttk.Button(
        botones,
        text="Descifrar",
        command=lambda: descifrar()
    ).pack(side="left", padx=(0, 6))

    ttk.Label(marco_resultados, text="Entre comillas:").grid(
        row=3, column=0, sticky="w", padx=(0, 6)
    )

    ttk.Entry(
        marco_resultados,
        textvariable=var_mensaje_comillas,
        state="readonly",
        font="TkFixedFont"
    ).grid(row=3, column=1, sticky="ew", pady=2)


    tabla = crear_zona_detalle(pestaña, [
        ("N.º", 45),
        ("Bloque c (antes)", 130),
        ("Calculo c^d mod n", 230),
        ("Bloque m (despues)", 130),
        ("ASCII (3 digitos c/u)", 150),
        ("Caracteres", 150)
    ])












    #ACCIONES

    def descifrar():
        nonlocal ultimo_resultado

        limpiar_resultados()
        texto = txt_cifrado.get("1.0", "end-1c")

        try:
            resultado = descifrar_mensaje(
                texto,
                var_longitud_entrada.get(),
                var_p.get(),
                var_q.get(),
                var_e.get()
            )
        except ErrorRSA as error:
            lbl_error.configure(text= str(error))
            return
        except Exception as error:
            lbl_error.configure(text= str(error))
            return

        lbl_error.configure(text="")
        ultimo_resultado = resultado
        mostrar_resultado(resultado)



    def mostrar_resultado(resultado):
            parametros = resultado["parametros"]
            n = parametros["n"]
            phi = parametros["phi"]
            d = resultado["d"]

            mensaje = resultado["mensaje"]
    
            var_d.set(str(d))
            var_n.set(str(n))
            var_phi.set(str(phi))

            var_longitud.set(str(resultado["longitud"]))

            #revisar---------------------------------------------------
            var_relleno.set(
                "Si (se quito el ultimo espacio)"
                if resultado["hay_relleno"] else "No"
            )

            escribir_texto(txt_mensaje, mensaje)

            var_mensaje_comillas.set(
                f'"{mensaje}"   ({len(mensaje)} caracteres)'
            )

            filas_tabla = []

            for fila in resultado["filas"]:
                filas_tabla.append((
                    fila["numero"],
                    f"{fila['c']:06d}",
                    f"{fila['c']}^{d} mod {n} = {fila['m']}",
                    f"{fila['m']:06d}",
                    f"{fila['codigo1']:03d} {fila['codigo2']:03d}",
                    fila["caracteres_txt"]
                ))

            llenar_tabla(tabla, filas_tabla)
    
    def cargar_datos(texto_cifrado, longitud, p, q, e):
        limpiar_todo()

        txt_cifrado.insert("1.0", texto_cifrado)

        var_longitud_entrada.set(str(longitud))
        var_p.set(str(p))
        var_q.set(str(q))
        var_e.set(str(e))
    
    def copiar_mensaje():
        if ultimo_resultado is not None:
            copiar_al_portapapeles(
                pestaña,
                ultimo_resultado["mensaje"]
            )
    
    def limpiar_resultados():
        nonlocal ultimo_resultado
        ultimo_resultado = None

        escribir_texto(txt_mensaje, "")

        llenar_tabla(tabla, [])

        for variable in (
            var_d,
            var_n,
            var_phi,
            var_longitud,
            var_relleno,
            var_mensaje_comillas
        ):
            variable.set("")
    
    def limpiar_todo():
        limpiar_resultados()

        lbl_error.configure(text="")
        txt_cifrado.delete("1.0", "end")

        for variable in (
            var_longitud_entrada,
            var_p,
            var_q,
            var_e
        ):
            variable.set("")

    # DEVOLVER PESTAÑA Y FUNCIONES NECESARIAS
    return pestaña, cargar_datos




    
vantana = tk.Tk()
vantana.title("PROYECTO RSA")
ancho = min(1100, vantana.winfo_screenwidth() - 80)
alto = min(900, vantana.winfo_screenheight() - 100)
vantana.geometry(f"{ancho}x{alto}+20+20")

vantana.cuaderno = ttk.Notebook(vantana)
vantana.cuaderno.pack(fill="both", expand=True, padx=8, pady=8)

#vantana.pestaña_descifrar = PestañaDescifrar(vantana.cuaderno)
vantana.pestaña_descifrar, vantana.cargar_datos_descifrar = crear_pestaña_descifrar(
    vantana.cuaderno
)

def enviar_a_descifrar(texto_cifrado, longitud, p, q, e):
    vantana.cargar_datos_descifrar(
        texto_cifrado, longitud, p, q, e
    )
    vantana.cuaderno.select(vantana.pestaña_descifrar)

vantana.pestaña_cifrar = crear_pestana_cifrar(
    vantana.cuaderno,
    enviar_a_descifrar
)


vantana.cuaderno.add(vantana.pestaña_cifrar, text="Cifrar")
vantana.cuaderno.add(vantana.pestaña_descifrar, text="Descifrar")


vantana.mainloop()


"""
⠐⢢⠱⡙⢦⢓⠲⡰⢀⠆⢠⠐⠰⡈⠔⡂⠔⡀⠆⡰⢀⠆⡐⠠⢂⠰⠐⢂⠅⠂⠄⠠⠀⠄⠠⠀⠄⡀⠠⠀⠄⠐⡀⠎⠰⢁⠒⡈⠐⠠⠑⢈⠱⠈⠜⠠⠃⡘⠠⠃⠜⡐⠂⠖⠰⡀⢂⠐⡀⢂⠐⠤⡀⢂⠄⢠⠀⠄⠠⠐⠠⢒⠰⡀⠆⠠⢀⠂⠄⠄⡠⢀⢀⠠⢀⡀⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠄⠠⠀⠄⠀⠀⠀⠀⠠⠀⠄⠠⠀⡄⢂⠤⡀⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠠⠀⠠⠀
⠀⠂⢡⠘⢄⠊⡑⠰⢉⠐⠂⠌⡐⢌⠢⠑⡠⠒⠠⠁⠆⡐⠠⠁⢂⠂⡉⠄⠨⠁⠌⠠⠁⠌⡐⢁⠂⠄⡁⠂⠈⢀⠐⡈⢁⠂⠡⠐⠠⠀⠀⠀⠀⢈⠀⠄⢀⠀⠀⠄⠀⠀⠈⠠⠁⠐⠀⢂⠐⠠⠁⢂⠐⠠⠈⠄⠈⠄⠁⠀⡁⢂⠑⡐⢈⠐⡠⢈⠐⡈⠰⡀⠎⡐⢂⠔⡨⠘⠤⣉⠒⡄⢂⡐⠈⠄⠂⡁⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠂⠈⢀⠁⠀⠀⠀⠀⠈⠄⠡⠈⠄⡑⢠⠃⡖⢡⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠄⠀⠄⠁⠀
⠀⡈⠄⠌⢂⠡⢀⠃⡐⢈⠐⠠⠈⡄⢃⠧⢠⠁⢂⠁⠂⠄⡁⢂⠰⢈⡐⢈⠄⡁⢂⠐⡀⠒⡈⠤⠈⠄⠠⠀⠁⡀⠐⡀⠂⠌⠄⣁⠂⠡⠀⠂⠈⢀⠈⡐⠠⠀⠌⠀⠐⠈⡀⠄⠠⠐⠈⠀⡐⠠⠀⠀⢈⠠⢁⠀⠀⠀⠀⠀⠀⠀⠂⠀⠂⠐⢀⠂⠌⡀⢣⠘⠤⡑⢌⢢⠡⢍⠒⡠⠡⠘⠠⢌⠱⣈⠱⠐⡂⢌⠂⠥⢈⡐⠠⠀⠄⡀⠂⢁⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠂⠁⠂⠐⠠⠑⡈⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⡀⠀⢀⠂
⠐⠠⢈⠐⡈⡐⠂⠌⡐⠠⠌⠠⠁⠠⢁⠊⡐⠈⠄⡈⠐⡠⠐⡠⢑⠢⢌⢂⠒⡄⠢⡐⠠⡑⡈⠄⠃⠌⠐⡀⠁⠀⠐⠠⢉⡐⠈⠄⡈⠄⠡⠀⢀⠀⠂⠄⠡⢈⠀⠂⠁⡐⢀⢂⠁⣀⠆⠑⡈⠡⢌⡑⢪⡐⢡⢂⡀⠀⠤⣀⠀⠄⠀⠀⠀⠐⠀⠀⠀⠀⠀⠉⠐⠡⠊⠤⡙⢌⠓⡤⢃⠡⣁⠂⢒⠠⠡⢈⠐⠠⠊⠄⠡⡀⢃⠍⡰⠠⢁⠂⡈⠄⡐⠠⢀⠂⡀⠄⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠐⢀⠀
⠈⡐⢀⠂⡐⠠⠁⠂⠄⠡⠈⠐⠈⠀⠠⠐⢀⠁⠂⠄⡡⠄⠱⣀⠣⡘⢄⠢⡁⢆⠱⡈⢅⠰⢈⠰⠁⠌⡐⠀⠄⠀⠡⡘⡰⢀⠃⡐⠠⠈⠄⠀⡀⠠⠁⠌⠠⠀⠠⠀⡁⠀⢀⣈⠒⠉⢚⡐⠄⡁⠠⠉⠣⠘⠁⠊⠉⠒⠠⢌⠘⡌⢂⠀⠀⠀⡀⠀⠀⠀⠀⠀⠐⠀⠁⠂⠌⠄⢣⠐⣉⠒⠤⣉⠢⣁⢃⢂⠩⡐⠡⢌⡐⠠⠈⠄⡁⢃⠂⠡⠐⡂⠤⢁⠆⡰⠠⠌⣀⠂⠡⠐⡀⠌⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠂⠈
⠠⠐⡀⠠⠀⡐⠈⡐⠈⠤⢁⠂⠄⡁⠄⠂⠄⣈⠐⡈⠄⡘⢠⢂⠱⡈⠆⠡⠌⡀⢃⠘⡠⢃⡌⢢⢉⡐⠠⠈⢀⠀⠡⢐⠡⢃⡐⠠⠁⠌⠀⡀⢀⠂⠡⠌⠠⠁⣀⣤⡴⠎⠟⣘⣉⣤⣤⣴⣶⣶⣶⣶⣶⣿⣿⣿⣿⣿⣿⣾⣷⣦⣅⣊⠐⠀⠀⠑⠬⡄⠀⠀⡄⠀⠀⠐⠤⡈⠀⠘⠤⣉⠒⡄⢡⢂⡌⢆⡣⣍⡓⢆⡘⠤⢁⢂⠐⠠⠈⠄⠡⢈⠔⠡⠘⣀⠣⡘⢄⠊⡅⠒⡄⢂⠌⡀⠄⢂⠐⠠⠀⠄⡀⡀⠀⠄⠠⠀⠄⠠⠀⠄⡀⠄⢀⠁
⡥⣃⠔⡠⠐⡀⠐⠠⢁⠂⠄⡈⠐⠠⠐⢈⠐⢠⠘⣀⠒⡀⠆⢌⠢⡑⢌⠡⠒⡀⢂⠐⠀⠣⣜⢣⠳⣌⢧⡘⡤⣈⠔⡀⠣⢄⡐⢠⢁⠂⡁⠀⠀⡈⠐⢀⣴⡶⢟⣩⣴⣾⣿⣿⣿⣿⣻⣿⣿⣿⣿⡿⢿⣯⣭⣝⣛⡛⠻⠿⢿⣿⣿⣿⣿⣿⣶⣤⣄⡑⠂⠀⠸⡁⠀⢀⠀⠡⠀⠐⠠⠀⢣⠈⡄⢂⠘⢄⠳⢌⡱⢊⠐⡄⠃⡄⠊⠄⡁⢂⠁⠢⠌⢂⠅⡠⠒⠠⠌⠒⡈⠡⢐⠈⡐⡐⢈⠂⡉⠆⡉⠦⡑⣌⠱⣈⠱⡈⢌⠡⡘⠠⠐⡈⠠⠀
⡳⣭⢲⡡⠒⡌⢡⢃⢮⡘⢦⠡⡍⢢⠁⠆⡌⢂⠒⡄⢒⠰⡈⢄⠢⡁⢌⠢⢑⠠⠂⡄⢀⠠⣌⢣⡛⣜⢲⣙⠲⡁⠆⠐⢡⠒⡌⠒⣌⠳⡐⠂⣁⣴⣶⣿⣿⣾⣿⣿⣿⠿⣛⣫⣭⡼⠿⠿⠟⠛⠿⠶⠖⡶⣶⣾⣾⣭⣽⣛⣳⢶⣮⣭⣭⣭⣛⡿⢿⣿⣿⣶⣄⡁⠀⢋⠀⠀⠈⠄⡀⠀⠀⢣⠔⡡⢈⠄⡂⢆⠰⡀⢃⠄⢃⠄⢃⠐⡀⠂⠌⢡⠘⡀⢢⠐⡡⠃⡜⠠⡁⠆⡁⠢⠐⡀⠆⡐⢀⠂⡁⢂⠑⠨⡑⠌⠱⡘⢌⠢⢡⠑⢢⠐⣁⠂
⣗⣣⢇⡳⢩⡐⠡⢎⢲⡙⣎⠱⡘⠤⣉⠒⡌⣡⠓⣌⠣⢒⡉⠦⡑⣌⠢⣑⢊⡔⢣⠜⣣⢗⣮⣷⣻⣬⢳⣌⠣⠐⠀⠈⠄⠒⡈⠔⠠⠃⠀⡶⢉⣿⡿⢋⣼⣿⡿⠟⣛⣫⣭⣤⡶⠾⠿⢶⡛⠡⣍⠡⣍⡫⣍⠛⢿⠿⣷⣾⣭⣭⣟⠻⢿⣿⡿⢿⣿⣿⣿⣿⣿⣿⣶⣄⠈⠂⠀⠀⠰⣀⠀⠀⠈⠔⡁⠢⠌⡐⢂⠁⠆⡈⠆⡈⠄⠂⠄⡑⠈⠄⠂⠄⠡⠘⡀⠣⠐⡡⠐⠌⢠⠡⢁⠒⠠⠐⡀⢂⠐⠠⢈⠐⡀⠌⠐⡀⢂⠁⢂⠩⢀⠣⢄⠣
⢗⡞⣼⢱⢃⡌⠱⡈⠦⡑⢮⡱⣉⠖⡤⢓⠬⣐⠣⢆⡹⢠⡙⢢⠱⣄⠳⣌⠲⡘⢤⢋⡖⣏⢾⡱⣟⣼⢳⣬⢣⡑⠤⡁⢎⢡⠒⠈⠀⢀⡝⣰⣿⠏⣱⡿⢏⣥⠖⣿⠛⠛⢉⣁⡤⠍⠩⠄⠀⠁⡄⠳⢠⡗⢈⣿⠾⠁⣿⣯⠹⣿⣿⣯⢿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣧⣄⠀⠀⠀⠀⠆⠀⠀⠀⠐⢁⠂⠰⢀⠊⠤⠑⡠⢡⠘⡀⠒⠠⠉⡄⢡⠈⢄⠡⢀⠁⠂⠄⠁⠌⡀⢂⠐⡈⢁⠂⡐⠄⢊⠐⡀⠂⠄⡈⠄⠐⠀⡈⠄⢂⠐⡀⢊⠐
⢎⡼⣜⡣⢧⢌⡱⣈⠖⡩⢆⡵⡉⢎⡱⡉⢖⢡⢋⠦⣡⠣⡜⣥⠓⡤⢓⠬⣓⡹⢦⡩⢞⡼⢣⡝⡜⢮⡳⣎⠷⣩⢒⡱⢊⠖⠁⠀⠀⣬⣴⣿⠇⣰⠷⠀⣋⣴⠎⢋⡈⠰⠈⠀⠀⠀⢀⠀⠀⠀⠀⠀⠐⠼⣈⢿⣧⣾⣿⣿⣇⣿⣿⣿⣜⣿⣿⣃⡍⢯⣡⢞⠊⢿⠥⢤⡙⠌⣷⡀⢂⠀⠈⠂⠀⠀⢂⠀⢌⡁⠆⠌⡰⠁⡔⠂⠤⠁⡌⠄⠡⠐⠂⠌⡀⠎⡐⠌⡐⠠⢁⠂⡐⢀⢂⠐⡀⢂⠐⡈⠄⠂⠄⡁⢂⠐⡈⢀⠂⠀⠄⠂⡐⠀⠂⡀
⢞⡼⣎⡷⣹⢎⡶⣱⢮⡵⣣⠖⣍⢦⡱⣍⣎⠶⣡⢒⡡⢒⡉⢆⠫⡔⡩⢞⣱⣛⢦⡙⠦⡘⣅⢚⡬⢣⠽⣘⠣⠁⠏⠴⠉⠀⠀⢀⠞⣭⢳⠃⠔⢡⣴⣾⠟⣡⣞⣤⣠⠄⣤⠈⠈⡑⠂⠆⡠⢀⠀⠀⢂⠤⠀⣄⡘⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⡏⠻⠄⠻⣮⡑⡄⠐⠂⠞⠣⠘⢿⣆⡀⠀⡁⠈⡄⠈⢆⠀⡎⡔⡡⢄⠃⠤⠑⢂⠡⡐⠌⡠⠡⠌⡐⡐⢢⠁⢎⠰⢁⢂⠒⠠⠌⡀⢂⠐⡀⢂⠐⡈⡐⠠⠀⠄⠂⠐⠀⠠⠈⡀⠂⠄⡁⠂⠄
⣽⣳⡝⣾⢱⢫⢞⡵⣳⢯⣳⡻⣜⡲⡽⡹⢞⣻⢧⡟⣴⢣⡜⣮⡱⣬⡑⣎⠴⣩⠲⣍⡖⣱⣬⢳⡜⢣⡑⠌⡐⠉⠰⠈⠀⠀⠀⠌⠒⡴⠣⠊⣴⣿⣿⣯⣾⣿⣿⡿⢻⡟⡔⢣⠒⡁⠁⠀⠀⠀⠡⠀⠀⠈⠣⣄⠳⡘⢾⡿⢿⣿⣿⣿⡿⣿⣿⣿⡌⣟⢆⡀⠙⠈⠣⠀⠀⠀⠈⠀⢺⡧⠀⠀⢀⠂⠀⠈⡆⢱⡹⣜⢮⡙⢦⣉⢆⡱⢌⢢⡑⣌⠢⡑⠌⡆⡙⠤⢁⠂⠂⠌⡐⠠⠐⠠⢀⠐⡀⠂⠡⢀⠡⠈⠄⠂⢀⠂⢁⠐⠠⠁⠂⠀⡁⠂
⠲⢧⢻⡜⢣⠏⡼⢸⡱⢏⠷⣏⡳⢱⢣⡙⢮⡱⢫⡜⣣⠯⣝⡶⣻⢵⣫⢎⡷⣥⢻⣜⣿⣳⢏⡟⠼⣡⢒⡴⣠⢌⡐⠀⠀⠀⠠⠀⠁⠈⠀⢬⣿⣿⣿⣯⡙⣉⡭⡙⠋⠈⠁⠀⡀⢀⠀⠀⠀⠀⠀⠀⠀⠀⢁⠂⠡⢃⢪⠑⠸⢻⣿⡿⢓⣿⣿⣿⠻⠒⣣⠖⠤⠂⠤⢠⠲⡍⢟⣧⡀⢹⡄⢠⡄⠀⡀⠀⢁⠠⡑⢎⠲⣉⠶⡩⢆⡳⢌⡳⡜⢦⠳⣌⠳⡌⠴⣁⠆⡌⢡⠂⠄⢡⠈⠔⡀⢂⠠⠁⡐⠀⡀⠂⠈⠐⡀⠐⠠⢈⠐⠀⠀⡀⢀⠂
⣹⣟⣶⣝⠪⡜⡱⢧⡹⢌⠳⣌⠱⡃⢆⡹⢄⠳⡡⠎⢥⣛⡼⣳⡝⢮⣓⠻⣞⣷⣻⣾⢯⣿⣎⡜⡑⢢⡙⢾⣟⡏⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⢋⡍⠣⠟⠀⠁⢠⠐⠈⠁⠈⠀⠁⠀⠤⢀⠀⠀⠄⡀⠀⠩⠀⢚⠀⠀⢀⣻⣿⣧⠘⣿⣿⠃⡠⠏⠁⠄⠂⠁⠀⠀⠁⠀⠘⠸⢿⣦⡁⠿⡄⠀⠐⢄⡂⠀⢌⢂⠓⣌⠲⡙⢮⢱⢣⠖⡩⢆⠣⣌⠳⡜⡳⣌⠖⡸⢄⠎⡘⢄⠊⡔⢡⢂⠤⡁⠐⠠⠐⡀⢁⠠⠀⠈⠀⠀⠠⠀⡁⠐⠠⠌
⠘⢏⠛⡌⠑⡈⡑⠢⢑⢊⡱⢌⡓⡘⢆⠱⢊⡱⠰⡉⠦⡙⠲⡁⢎⡱⢌⠓⡜⡰⢃⠏⡿⢳⢎⠴⡑⢢⢈⡑⢎⠁⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣯⣀⠋⢠⡟⠀⠀⠲⠈⢀⠀⠆⢀⢀⣀⡀⣀⠈⢓⡆⠀⡐⠀⠀⠀⠀⡀⢀⣾⣿⣿⣿⣿⣦⡀⠰⠋⢀⠄⠂⠀⠀⣀⠄⠠⠤⡀⠀⠈⢻⣿⣆⠡⠀⠀⡸⠀⠐⡌⢎⡱⢀⠣⡘⢂⠇⡎⡜⡱⣊⠖⣌⡱⢬⠱⣎⠝⡱⢋⢮⡱⢌⠲⢌⡱⢊⡔⡡⡉⢆⠡⡐⢢⠐⡴⣠⢆⡤⣁⠐⠠⢁⠂⠄
⠈⠄⠡⢀⠡⠐⡀⢁⠂⠄⠐⠂⡘⠐⡈⠌⡁⠒⠡⠌⠠⠁⠡⠈⠄⡐⢈⠒⠠⠑⡈⠘⠰⡉⢎⠒⣉⠖⢢⠐⠂⠀⠀⠀⠀⠀⠀⠀⠀⣺⡿⣿⣯⠥⠴⠻⠁⠀⢃⣠⣶⣿⣷⣶⣶⣦⣤⣶⢿⣷⡀⠈⠆⡀⠀⠀⠀⠘⣁⣾⠏⢹⣿⣿⣿⣿⣆⠀⢠⠜⠀⢠⠒⡂⠀⠀⠀⠀⠀⠁⢀⠀⠉⣿⡆⠀⠀⠘⠁⠄⠘⠠⠑⠈⠄⡑⠈⠜⠰⡁⠧⡙⢮⡑⢎⢣⡛⡼⣎⠵⣉⠦⡙⢎⡱⢊⠖⣭⠲⣅⠳⣈⠆⡑⢢⠙⡜⠳⡞⣵⢣⣯⡱⢆⡜⡠
⠀⠈⢀⠂⠄⡁⢀⠂⢀⠀⠂⠐⠀⠁⡀⠄⠀⢁⠠⠀⠐⠀⠁⠠⠀⠄⠠⠀⡁⢀⠀⠁⠂⠐⡈⠐⡀⠊⠄⡈⠀⠀⠀⠀⠀⠀⠀⠀⢠⡿⣽⣩⣶⣶⠏⣡⠶⢿⡍⠭⣭⣥⣼⢻⣏⣙⡛⠻⢦⠼⣡⠀⠠⣵⣤⡤⢠⣶⣿⠏⣸⣾⣿⣿⣿⣿⣿⣦⠀⠠⠀⢀⣴⡿⡷⠄⡤⠲⠀⢀⠈⠆⠀⡘⣷⠀⠀⠀⢞⡱⣂⠁⠀⠀⠀⠠⠁⠈⠐⢈⠰⢉⠆⡘⢄⠣⢜⡱⣭⢛⡴⢣⠍⡆⢥⢋⡜⠤⠛⣌⠱⡄⢎⠰⡁⠜⡨⢱⡘⢆⢏⠲⣙⠳⢎⠷
⠀⠌⡀⠄⠂⠐⠠⢀⠂⠠⠐⠀⠌⢀⠀⡀⢈⠀⠠⠐⠀⡈⠄⠡⢈⠐⡀⠁⠄⡀⠀⠠⠈⡀⠄⢁⠠⠁⠂⠀⠀⠀⠀⠀⠀⠀⠀⢀⢺⣿⣿⣛⣭⣶⣾⡿⣿⣭⣉⠥⣄⡌⣩⢉⡉⡉⠛⠳⢒⠂⠓⠛⢂⠽⢉⣴⣿⣿⠏⣴⣿⡿⠙⣩⣿⣿⣿⣿⣦⡀⣀⣌⣖⠳⢲⣷⣶⣷⣿⣷⣦⣄⡀⣿⣿⡄⠀⠀⢪⠴⡡⠎⡄⡀⢀⠀⠀⠈⠀⠀⠄⢈⠐⠌⡠⠓⣎⠵⣎⢧⠸⡥⢞⡜⢎⡖⠬⡑⠩⢄⠣⢜⡈⠖⡡⢊⠔⣡⠘⡄⢊⠐⠡⠘⡈⠐
⠀⢂⠐⠠⠁⠌⡐⠠⢀⡁⢂⠡⡈⢄⠢⢐⠠⣈⠐⣀⠂⠄⢂⠁⢂⠂⠤⢁⠢⢀⡁⢂⠡⠐⡈⠄⢂⠡⠌⡀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣵⣤⣦⣤⣡⣡⣀⠠⡈⣠⣤⣶⣾⣿⣿⣿⣟⣾⠏⢀⣴⣿⣿⣿⣿⣿⣿⣿⣷⡈⠖⠈⠄⢩⠹⢭⣿⣿⣿⣿⣟⣛⣽⣿⡇⠀⠀⢣⢣⠑⡘⠤⡑⢢⠐⡠⠀⠀⠀⠀⠀⠈⠐⡁⢣⠘⡜⠰⡊⠵⣈⠧⡘⢢⠘⠄⡁⠃⠌⡐⠂⠌⠠⠁⠌⠂⢅⡚⡔⣣⠜⡤⢃⡴⢡
⠀⠂⠌⡐⢈⠐⠠⠁⠂⠐⡀⠂⡁⢂⠁⠊⡐⠠⠈⠄⡈⠐⠠⠈⠄⠈⠐⠀⠂⠀⠐⠀⠂⠁⡐⠈⢀⠂⡐⠁⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣿⣿⣿⣿⣿⣿⣿⣿⠿⠋⣠⠋⡜⠳⠾⠿⠿⣬⠉⢿⢷⡉⣦⣄⣀⣀⢡⣤⣴⣶⣬⣩⣭⣿⣾⣿⣏⠀⢀⢣⠂⡍⠰⢡⠘⣄⠫⢔⡱⢂⠄⡀⠀⠀⠀⠀⠀⠱⢈⠱⢈⠆⠡⢂⠑⢂⠩⠄⡑⡈⡐⠠⠈⠄⡁⠂⡄⣁⠢⠐⡱⢨⠙⡜⠱⣊⠳
⢈⡐⠠⢀⠂⢈⠀⠄⠁⠀⠀⠐⠀⠠⢈⠀⡀⠀⠀⠂⢀⠡⠀⠀⠐⡈⠀⠀⠀⠀⡀⠐⡀⠄⡀⠐⡀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢋⣥⠖⠛⠁⠒⡈⠁⠌⢉⠱⠀⠂⢀⠪⠁⠘⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⢆⠩⡐⢉⠢⡑⢢⢍⢲⡐⢣⠘⠤⣁⢂⠀⠀⠀⠄⠀⠀⠂⠌⠡⠀⠌⠀⡐⢈⠐⡐⠠⡑⢌⠰⢀⠡⡐⢄⠢⡑⢄⠣⡐⢌⠱⣀⠣
⠢⡜⣐⠂⡌⢀⠂⠠⢀⠂⢁⠐⢈⠐⠢⠡⠐⡀⠀⠀⠀⠀⠀⢀⠂⢁⠁⢂⠀⠀⡐⠤⠐⢂⠑⠂⢀⡀⢀⠀⢀⠤⣄⠀⠀⡌⢰⢋⡞⣿⣻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠰⢋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⢂⠐⠠⠑⡌⢃⠎⡱⢌⠣⣉⠒⠤⢊⠜⠰⢠⢀⠀⠂⠀⠀⠁⠈⠀⢀⠀⢀⠂⠄⠡⠐⡈⠰⡈⠔⡡⢊⠴⡑⡊⡔⡉⠦⡑⠤⢃
⢱⡘⠴⣩⢒⠤⢊⠔⡂⢜⡠⢊⠄⠂⡁⠄⠡⢀⠡⠀⠂⠄⠁⡀⠄⢠⠈⡔⡈⠔⡐⠢⡁⢂⠈⡜⣱⠎⡱⠀⠁⠀⠈⡇⠀⠀⣎⢼⣹⢳⣝⡻⣞⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⢡⠃⡰⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀⡈⠠⢁⠘⠠⢊⠐⡀⠒⡠⢉⠆⡡⢊⠱⢌⠪⢜⡠⢄⠀⠀⠀⠀⠀⠀⠀⠈⠄⢃⡐⢁⠂⡱⢘⡰⣉⠶⡱⠱⢤⡙⢦⡹⢌⡣
⡅⢎⡱⣡⠫⣜⠡⢎⡘⢄⠢⠡⢌⠒⡰⢈⠒⡄⢂⡁⠂⠌⡐⢠⠘⡄⢣⠐⣌⠰⣀⢣⡔⣦⠃⢈⠀⠤⡁⠀⠀⠀⡄⢸⠀⢨⢟⡎⣯⢗⢮⠳⣍⠟⣧⢟⡿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠟⡛⠛⠛⣁⡴⠾⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⠹⠋⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠄⠀⠄⡁⠠⢈⠐⡀⠠⠀⠁⠄⡁⢊⠰⣁⠫⣌⢓⠢⡑⠬⡘⠤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠂⠐⠠⢁⠂⠡⢃⠍⡓⢦⡹⢦⡙⠦⡱
⡝⢮⡑⢆⠳⢌⢃⠒⡌⠢⣁⠣⠌⢢⠑⠌⡒⠌⢢⠐⡉⢆⡑⢢⡑⢌⠢⡑⠌⡱⢈⠆⣹⢂⡔⣠⠙⣦⠃⠀⠀⣸⣠⡄⠂⢈⡮⣝⣎⠿⣌⡓⢌⠫⡜⢪⡝⣹⢯⣿⣿⠟⣫⠽⠏⠉⠐⢀⣤⣶⣿⡟⢻⡇⢀⠠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠉⠻⠿⣿⣿⣿⣿⣿⣿⣿⣿⠀⢀⠂⠄⡁⠂⠄⠀⠄⢀⠈⢀⠠⠀⡐⢄⠫⡜⡌⡓⢌⠢⠑⡈⠄⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⢈⠐⠠⠊⡅⢣⠙⢢⠙⣢⠱
⡜⣡⠚⡌⡘⢄⠊⡔⢠⠡⡐⢌⠢⠡⢌⠒⡤⣉⠆⠥⡉⠆⡜⢡⡘⢬⠱⢌⠒⡄⢢⠘⢲⢫⢒⠡⢛⠰⠀⠃⢀⡏⣿⡷⠀⠈⢶⢩⡎⣟⠶⣩⠌⡑⢌⠣⡜⢥⡛⡜⢮⡙⠂⠀⠀⠠⡴⡿⢻⡿⠟⠁⠋⠁⠁⠀⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠤⡀⠀⠈⢿⣿⣿⣿⣿⣟⡳⠀⠀⠈⠐⠠⠁⠌⡀⢂⠠⠀⠂⢀⠐⡀⠎⠰⠐⡈⠱⠈⠄⠁⢀⠀⠂⠀⡀⠁⠐⡀⢀⠀⠀⠀⠀⠀⠀⠡⠁⠒⡈⠤⢁⠂⠡⢀⠃
⡰⣁⠞⡤⢩⠜⡒⢌⢆⡱⢌⠦⣉⠳⣌⢓⢲⡱⢮⡱⣘⠰⣌⠢⢜⢢⡙⢬⠱⡘⢤⢋⠴⣈⠦⡱⣈⠤⠀⠃⢸⠅⣹⠁⠀⠀⢊⢶⡹⠎⣳⠄⠑⢦⠨⠑⡌⠰⣍⢎⠑⠀⠀⠀⢠⠎⠓⠁⠉⠀⠘⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⣟⡶⡏⠀⠀⠀⠀⠁⠈⠐⡀⠂⠄⠐⠀⠠⠀⠐⠈⠄⠡⢀⠁⠌⠀⠈⠀⠀⠀⠀⠀⠀⠂⠀⠄⠂⡐⢀⠀⠀⠀⠀⠀⠀⠐⠐⠂⠌⠐⡀⠂
⠴⣈⠚⡤⢃⡚⣬⡘⢆⡜⣪⢱⡉⠖⡨⠌⢢⢙⠳⢲⠩⠳⢌⡑⢊⠦⣙⢆⢣⡍⠶⣩⠖⣭⢲⡱⢦⡹⡁⢸⣞⠀⢹⠀⠀⠀⢍⠶⠁⣘⡁⠆⡛⠌⠀⡹⢀⡳⠌⠂⠀⠀⡀⠔⠁⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠘⢿⣟⣾⣳⠅⠀⠀⠀⠀⠀⠀⠀⠀⡁⠂⠄⠂⠁⠠⠈⠐⡀⠂⡀⠠⠀⠠⠁⠀⠄⠂⠀⠀⠀⠀⠁⡀⢂⠐⠠⠊⡔⢠⠀⠀⠀⠀⠀⠀⠀⠂⠄⡁
⠦⣁⠏⠴⡩⢞⡱⡽⢮⣝⣧⠧⡘⠠⠐⡈⠄⡈⢡⠂⡁⢁⠂⡜⡈⠖⣩⢾⣿⡞⢧⢃⠞⠴⢣⡝⢦⠳⢥⠈⣏⣤⡈⠀⠀⠀⠈⡀⢸⠀⠁⢠⢃⠀⡰⢹⠐⣣⠁⠀⠠⠆⠁⠀⠈⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠆⠌⠄⠠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣞⣷⣏⠀⠠⢁⠂⡀⢀⠀⠀⠀⠀⠁⠐⠠⠁⠂⡁⢂⠐⠠⠐⠀⠄⠁⠠⠁⠀⡀⠄⠂⠀⠀⠀⠀⠀⠌⡐⠡⠌⢂⠌⣁⠂⠄⡀⠀⠀⠀⠂⠀
⢆⡱⡈⢇⠜⣠⠱⣌⣳⢎⠶⡡⠃⢁⠆⡐⢠⠘⣦⢳⡐⢂⠐⠠⠑⡈⠔⢫⠱⣌⢣⣞⡿⣖⡄⠚⢌⠳⣘⠈⢏⠁⠀⠀⠀⠀⢀⠀⠀⠀⡄⠈⠈⠠⢁⠇⡸⠀⠀⡔⠁⠄⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠠⠁⠂⠄⡀⠂⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⡦⠀⢡⠂⡔⢀⠂⡐⢀⠀⠀⠀⠀⠁⠠⢁⠐⠠⢈⠐⠠⠁⠌⠠⠁⡀⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠄⠡⠘⡀⢂⠄⠨⠐⡠⢁⠆⢠⠀⠀
⢢⠱⡘⣌⠲⡡⠞⠽⠟⠏⠂⢠⠰⢌⠰⣀⠃⡜⢠⠃⡔⡈⠔⡡⠒⣌⠰⢂⠧⡘⠧⣚⠱⡰⢌⠣⣌⠳⣌⠐⣄⣁⡠⠀⠀⠀⢨⡀⠐⠈⠠⢂⠁⡔⠃⠖⠁⠀⠜⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠀⠀⠀⠀⠀⠀⠀⠐⠀⠀⠀⠀⢀⠀⠰⠀⠀⠀⠀⠀⠀⠀⠡⠄⠀⢢⠑⡌⢂⡒⢄⠂⠄⡀⠀⠀⠀⠀⠀⠌⠐⠠⠈⠄⠡⠈⠄⡁⠠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⢁⠂⠌⠠⠑⡠⠃⡜⢠⠃⢆
⢂⠧⡱⢈⠖⡡⢃⠤⡠⢔⢪⡑⢎⡜⢢⡑⢎⠴⣡⢚⢤⡑⢎⡔⣩⠔⣣⢍⢢⡑⢎⡔⢣⡑⢎⡱⢌⠳⡨⢄⠉⠏⠁⠀⠀⠀⠄⠀⠀⠂⠀⢈⠤⡐⢂⡀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠐⡂⠀⠢⢍⠰⠡⠘⢂⠁⠂⠄⢂⠡⠀⠀⠀⠀⠀⠁⠈⠄⠡⠈⠄⡐⠀⠄⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠈⠠⠁⢂⠁⠒⡈⠤⡉⠄
⠌⡆⠱⡈⢆⢡⠋⡖⢭⠎⡦⣙⠦⡘⢥⠚⣬⢚⡴⣋⠶⣩⠖⡼⣡⢟⡦⢏⠶⣩⢖⡬⠣⢜⠢⢜⢢⢃⠷⡘⢆⡀⠀⠀⠀⠀⢂⠐⠀⠀⠰⢉⠂⢔⠣⠀⠐⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠡⠀⠐⡈⠄⢂⠁⡎⡔⣩⠐⡄⠂⢁⠐⠀⠀⠀⠀⠈⠠⠑⡈⡐⠠⢈⠀⡐⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⢀⠠⠈⠄⡁⠒⡈⠔
⠳⣌⠣⣕⢊⠦⣙⢸⡘⣾⣱⣎⢮⠱⣊⠵⣊⠷⡸⢥⡛⡴⣋⠶⣙⠮⡜⣭⢚⡵⡚⡼⡑⣎⡱⢎⠶⣩⢞⣙⢮⡱⠀⠀⠀⠀⠈⠂⠀⣘⠀⠉⠐⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⣀⢀⡀⢀⡀⣀⢄⡠⣀⢄⡠⢀⣀⣀⢀⡀⢀⠀⠀⠀⠀⠀⠀⢂⠀⠀⠀⠀⠀⠀⠄⠀⠐⡈⢆⡱⢘⠲⣅⠳⢠⠁⢂⠈⡐⠀⠀⠀⠀⠀⠀⠐⠠⢁⠂⡐⠀⡐⠈⠀⠐⠀⠀⡐⠀⠁⢀⠀⠀⠄⠀⡀⠀⢂⠐⡈⠐⡐⢈
⠱⣊⠳⣌⠳⣘⠴⣣⢟⡳⢏⡞⢆⠧⡑⢮⠥⢫⣑⢣⡙⢴⢩⢚⠥⣋⠶⣘⠲⣌⠳⣅⠫⣔⢣⢏⡞⡱⢎⡎⢇⠣⠄⠀⠀⠀⠀⠀⠡⡈⢄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡁⢂⠄⡄⠢⠐⢦⡑⢊⠇⠓⡌⢧⠹⣃⡙⠣⣌⣁⢛⡎⡷⢫⡾⣽⢯⣿⢯⡟⣞⢦⣤⢲⠠⠁⠆⠀⠀⠀⠀⠀⠀⠀⠀⠈⢆⠢⢉⠒⠄⢃⠂⠡⢂⠐⠠⠐⠀⠀⠀⠀⠀⠀⠀⠀⠂⠄⡁⠀⠀⠈⠀⠄⠁⢀⠠⠈⠀⡀⠂⢀⠂⢀⠡⠀⠄⢀⠁⡐⠠
⠱⡌⠳⣌⠳⣌⢏⢧⢫⠜⣱⠚⡼⣘⠭⡲⢍⡳⢌⢦⡙⢆⠣⢎⠲⣡⠒⡥⣓⢬⢳⣬⢓⣎⠳⢎⡜⡡⢇⡜⡈⠡⠀⠀⠀⠀⠀⠀⠀⢰⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠡⠐⣂⠢⡌⣅⢚⡰⢌⣣⠀⣞⠡⣏⠞⡄⠉⢇⠀⠢⠈⡜⢡⠋⡁⠋⠎⡘⠫⣝⠫⣾⣱⢫⣜⠂⠈⠀⠀⠀⠀⠀⠀⠀⢁⠊⠄⡑⠠⠀⠌⠠⢈⠐⡀⠌⠀⠄⡀⠄⠀⠀⠀⠀⠀⠀⠀⠀⠠⠁⠐⠀⠁⠀⠄⠀⠠⠐⠀⡀⠐⠠⠐⡀⠄⠂⠀⠂⠀⡀⠄
⡱⢌⠳⣌⠳⡜⢎⠮⡱⢎⡕⣋⠶⡩⢖⡙⣎⡱⢎⠦⡙⣌⠳⣎⢳⢆⡻⡴⣋⣞⢣⢎⡳⢌⡙⠦⢌⡑⠢⠐⠀⠁⠀⠀⠀⠀⠀⠀⠀⣈⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠂⢨⠑⣢⠓⡸⠄⢃⠜⠂⠀⡘⠈⡀⠌⠒⠀⠁⠈⠐⠀⡀⠌⠀⡐⠈⠀⠀⠁⠄⠸⠐⡤⣉⠳⣎⢳⡀⠀⠀⠀⠀⠀⠀⠀⠀⠌⡐⠠⢁⠊⠤⢁⢂⡐⠠⢀⠁⠂⠄⠀⡈⠀⠄⢀⠀⠄⡠⠀⠀⠀⠂⠈⡀⠈⠀⠌⠀⠄⠂⠀⠌⡐⠠⠀⠄⠂⠁⠠⠐⠀⡀
⠴⣉⠶⣡⢛⢬⢣⠣⣕⠪⡜⣘⠖⣩⠚⣔⢣⠞⣬⢳⡹⣞⡽⣎⡟⢮⡳⣍⠳⣌⠣⢎⡐⢣⠘⡐⠂⠌⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠄⡡⠚⠤⢡⠁⡀⠎⠀⠀⠀⠀⠀⠀⠄⠀⠌⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⡴⢐⡳⢬⡜⣱⣃⠀⠀⠀⠀⠀⠀⠀⠈⣆⠡⢂⠅⡊⠔⡡⢂⠄⢣⠐⡨⠐⡈⠀⠄⡐⠈⡀⠌⡐⣁⠊⡄⠀⡄⢂⠄⢁⠐⠀⠂⠠⠈⡐⠠⠐⡀⠡⠀⢀⠂⠁⡀⠂⠄
⣒⢡⢚⡤⣋⢦⢣⠓⣌⠳⣌⠱⡊⠔⣭⢊⢦⡙⣦⢏⡷⡹⢞⡬⣙⢆⠳⡌⡓⢌⠒⠤⡘⠄⠃⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⢠⠁⠊⠔⠂⡀⠆⠀⠐⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠁⣔⠫⣁⠳⡜⣠⠇⠂⠀⠀⠀⠀⠀⢀⡼⡧⢏⡖⢬⠐⡡⢂⠅⡊⢄⠣⢐⠡⢂⠍⡐⣀⢂⠐⣀⠣⣟⡿⣜⠡⠘⠂⠌⡀⠠⠐⠈⢀⠡⢀⠁⢂⠐⠀⠐⠀⢀⠐⢀⠁⠂
⡜⢢⣏⠶⡝⡎⠥⠋⠴⢣⠜⠀⣠⠚⣤⢋⢦⡙⢦⣋⠶⡙⣌⠒⡥⢊⠵⣈⠱⣈⠜⠢⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠁⠀⠀⠂⠐⠀⠀⡀⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⢈⠤⣀⠓⢌⠐⡀⠀⠀⠀⠀⠀⠀⠀⢍⡻⣝⠾⣥⣏⠴⡁⢎⡘⢄⠣⠌⡐⡈⠤⢑⠠⢊⡔⢀⠂⠌⡙⠌⠂⢁⠈⢀⠠⢀⠀⡐⠀⠂⠌⡐⠠⠀⢈⠀⠄⠂⡀⠂⠌⡐
⡜⢣⢎⣽⣸⣵⣩⣽⡟⠁⢀⠢⣥⢛⡤⣋⠶⡙⡆⡇⢧⠱⡌⢚⠰⣉⠒⡌⠱⡐⠌⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠄⠀⠄⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠀⠀⠂⢁⠀⠂⠀⠈⠀⠀⠀⠀⠀⠀⠀⣀⠑⠎⠿⣼⢯⡗⣍⠢⠜⡠⢃⡜⢠⠑⢢⠡⢎⡥⡘⢤⡈⠔⡠⠈⠐⠠⢀⠠⢀⠂⠴⡐⢄⠈⠀⠄⠐⡀⠠⠀⠄⠂⠄⡁⠂⠄
⣜⣻⡾⣯⣟⣾⡟⠁⠀⢠⣌⠳⣜⢣⢎⡱⢊⠵⡘⠜⣂⠓⡌⢡⠒⠄⠣⢌⠑⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡐⠂⠡⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠻⣶⣤⣉⠳⡝⢦⡙⢬⡑⢦⠘⡤⢉⠦⡙⢎⠖⡩⢆⠸⡱⢧⡏⡔⣁⠂⡐⠠⢈⠐⡉⠄⡈⠀⠠⠀⢀⠐⠀⡈⠐⠠⠀⡁⠂
⣼⠟⠼⡱⠿⠓⠀⠀⠌⠃⠈⠓⠈⠒⠨⠐⠉⠢⠉⠂⠅⠊⠄⠡⠈⠌⠁⠂⠀⠡⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠢⠐⠀⢈⠙⠳⠤⠁⡘⠦⠳⠌⠳⠌⠣⢆⠹⠌⠌⠱⠨⠑⠌⠢⠄⠔⠢⠓⠌⠱⠈⠖⠠⠂⠄⠀⠐⠈⠄⠀⠂⠀⠐⠀⠀⠀⠄
"""