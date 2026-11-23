# Proyecto de criptografía RSA
MM2015 – Matemática Discreta 1

## Integrantes
- Carlos de León 251630
- Alexander Carrera 25178
- Grupo: 4

## Descripción
Programa en Python con interfaz gráfica que permite cifrar y descifrar
mensajes mediante RSA. Muestra los parámetros, la conversión ASCII
y los bloques antes y después de cada operación.

## Requisitos e instalación
- Python [versión utilizada].
- Python debe tener disponible Tkinter.
- No se utilizan bibliotecas externas; no se requiere instalar
  dependencias mediante pip.

## Ejecución
Descomprimir el proyecto, abrir una terminal en su carpeta y ejecutar:

```bash
python main.py
```

En Windows también puede utilizarse:

```bash
py main.py
```

O también pueden ejecutarlo dentro de Visual Code y esto lo hará automaticamente

## Cifrar
1. Abrir la pestaña Cifrar.
2. Escribir el mensaje e ingresar p, q y e.
3. Presionar Cifrar.
4. Consultar el texto cifrado en “Texto cifrado C” y la longitud
   en “Longitud original L”.
5. Conservar C y L para poder descifrar.

Los parámetros deben cumplir:
- p y q son primos distintos.
- 126126 < p × q < 1000000.
- e > 1 y MCD(e, φ) = 1.

Se admiten caracteres ASCII imprimibles del 32 al 126.
No se admiten tildes, ñ, tabulaciones ni saltos de línea.

## Descifrar
1. Abrir la pestaña Descifrar.
2. Ingresar C, L y los mismos valores de p, q y e usados al cifrar.
3. Presionar Descifrar.
4. Consultar el exponente privado d y el mensaje recuperado.

El botón “Enviar a Descifrar” copia automáticamente los datos
desde la pestaña Cifrar.

## Relleno y conservación de espacios
Cada bloque representa dos caracteres.
Si la longitud original es impar, se agrega un espacio al final.
Al descifrar, se utiliza L para comprobar y retirar únicamente
ese espacio de relleno, conservando los espacios originales.

## Ejemplo completo
- Mensaje original: "RSA"
- p = 367
- q = 373
- e = 17
- n = 136891
- φ = 136152
- L = 3
- Mensaje con relleno: "RSA "
- Bloques originales: 082083 065032
- Cifrado C: 026054 123875
- Exponente privado d = 8009
- Mensaje recuperado: "RSA"

## Algoritmos implementados
Todos se encuentran en main.py:

- es_primo: comprobación de primalidad.
- mcd: algoritmo de Euclides.
- inverso_modular: algoritmo extendido de Euclides.
- exponenciacion_modular: cuadrados y multiplicaciones con
  reducción modular durante el cálculo.

## Comprobaciones realizadas
Se Comprobaron:
- Mensajes de longitud par e impar.
- Mayúsculas, minúsculas, números y signos.
- Espacios consecutivos, al inicio y al final.
- Bloques cifrados con ceros iniciales.
- Rechazo de parámetros RSA inválidos.
- Rechazo de caracteres no admitidos.
- Rechazo de bloques mal formados o fuera de rango.
- Rechazo de longitudes inconsistentes.
- Recuperación exacta del mensaje original.

## Video demostrativo
https://youtu.be/kAWioy8Q1O4
En caso de problemas con el enlace el video esta en el zip