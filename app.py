
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

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Proyecto RSA", page_icon="🔐", layout="wide")
st.title("🔐 Proyecto de criptografía RSA")
st.caption("MM2015 – Matemática Discreta 1 · Grupo 4")
st.write("Cifra y descifra mensajes usando los parámetros RSA ingresados.")

for key, value in {
    "cifrado": "", "longitud": "", "p_c": "", "q_c": "", "e_c": "",
    "resultado_cifrar": None, "resultado_descifrar": None,
    "c_in": "", "l_in": "", "p_d": "", "q_d": "", "e_d": "",
}.items():
    if key not in st.session_state:
        st.session_state[key] = value

tab_cifrar, tab_descifrar = st.tabs(["Cifrar", "Descifrar"])

with tab_cifrar:
    st.subheader("Cifrar un mensaje")
    mensaje = st.text_area("Mensaje a cifrar", key="mensaje_c", height=100,
                           help="Solo se admite ASCII imprimible: letras sin tildes, números, signos y espacios.")
    col1, col2, col3 = st.columns(3)
    p = col1.text_input("Número primo p", key="p_c")
    q = col2.text_input("Número primo q", key="q_c")
    e = col3.text_input("Exponente público e", key="e_c")
    if st.button("Cifrar", type="primary", key="btn_cifrar"):
        try:
            st.session_state.resultado_cifrar = cifrar_mensaje(mensaje, p, q, e)
        except ErrorRSA as error:
            st.session_state.resultado_cifrar = None
            st.error(str(error))
        except Exception as error:
            st.session_state.resultado_cifrar = None
            st.error(f"Error inesperado: {error}")

    resultado = st.session_state.resultado_cifrar
    if resultado:
        parametros = resultado["parametros"]
        st.success("Mensaje cifrado correctamente.")
        st.text_area("Texto cifrado C (guárdalo junto con L)", resultado["texto_cifrado"], height=90, key="salida_c")
        a, b, c, d = st.columns(4)
        a.metric("Longitud original L", resultado["longitud"])
        b.metric("Relleno agregado", "Sí" if resultado["hay_relleno"] else "No")
        c.metric("Llave pública (e, n)", f"({parametros['e']}, {parametros['n']})")
        d.metric("φ(n)", parametros["phi"])
        filas = [{"N.º": f["numero"], "Caracteres": f["caracteres_txt"],
                  "ASCII": f"{f['codigo1']:03d} {f['codigo2']:03d}",
                  "Bloque m": f"{f['m']:06d}",
                  "Cálculo": f"{f['m']}^{parametros['e']} mod {parametros['n']} = {f['c']}",
                  "Bloque c": f"{f['c']:06d}"} for f in resultado["filas"]]
        st.dataframe(pd.DataFrame(filas), use_container_width=True, hide_index=True)
        if st.button("Enviar datos a Descifrar", key="enviar_descifrar"):
            st.session_state.c_in = resultado["texto_cifrado"]
            st.session_state.l_in = str(resultado["longitud"])
            st.session_state.p_d = str(parametros["p"])
            st.session_state.q_d = str(parametros["q"])
            st.session_state.e_d = str(parametros["e"])
            st.session_state.resultado_descifrar = None
            st.success("Datos copiados a la pestaña Descifrar.")

with tab_descifrar:
    st.subheader("Descifrar un mensaje")
    texto_cifrado = st.text_area("Texto cifrado C", key="c_in", height=100)
    longitud = st.text_input("Longitud original L", key="l_in")
    col1, col2, col3 = st.columns(3)
    p = col1.text_input("Número primo p", key="p_d")
    q = col2.text_input("Número primo q", key="q_d")
    e = col3.text_input("Exponente público e", key="e_d")
    if st.button("Descifrar", type="primary", key="btn_descifrar"):
        try:
            st.session_state.resultado_descifrar = descifrar_mensaje(texto_cifrado, longitud, p, q, e)
        except ErrorRSA as error:
            st.session_state.resultado_descifrar = None
            st.error(str(error))
        except Exception as error:
            st.session_state.resultado_descifrar = None
            st.error(f"Error inesperado: {error}")

    resultado = st.session_state.resultado_descifrar
    if resultado:
        parametros = resultado["parametros"]
        st.success("Mensaje descifrado correctamente.")
        st.text_area("Mensaje recuperado", resultado["mensaje"], height=100, key="salida_mensaje")
        st.code(f'"{resultado["mensaje"]}" ({len(resultado["mensaje"])} caracteres)')
        a, b, c, d = st.columns(4)
        a.metric("Exponente privado d", resultado["d"])
        b.metric("n", parametros["n"])
        c.metric("φ(n)", parametros["phi"])
        d.metric("Relleno retirado", "Sí" if resultado["hay_relleno"] else "No")
        filas = [{"N.º": f["numero"], "Bloque c": f"{f['c']:06d}",
                  "Cálculo": f"{f['c']}^{resultado['d']} mod {parametros['n']} = {f['m']}",
                  "Bloque m": f"{f['m']:06d}",
                  "ASCII": f"{f['codigo1']:03d} {f['codigo2']:03d}",
                  "Caracteres": f["caracteres_txt"]} for f in resultado["filas"]]
        st.dataframe(pd.DataFrame(filas), use_container_width=True, hide_index=True)

st.divider()
st.caption("Algoritmos educativos RSA · Se admiten caracteres ASCII imprimibles del 32 al 126.")
