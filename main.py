"""
Aplicacion web con Flask - Semanas V y VI
Autor: Pedro Loayza Forero

Menu principal con dos ejercicios:
  Ejercicio 1: promedio de 3 notas + asistencia -> aprobado / reprobado
  Ejercicio 2: 3 nombres -> el mas largo y su cantidad de caracteres
"""

from flask import Flask, render_template, request

app = Flask(__name__)

# ---------------------------------------------------------------------------
# Funciones de apoyo (logica en Python, separada de las rutas)
# ---------------------------------------------------------------------------

NOTA_MINIMA = 10
NOTA_MAXIMA = 70
NOTA_APROBACION = 40
ASISTENCIA_MINIMA = 75


def texto_a_numero(valor, etiqueta):
    """Convierte un texto del formulario a numero. Lanza ValueError si no se puede."""
    valor = (valor or "").strip().replace(",", ".")
    if valor == "":
        raise ValueError(f"Debes ingresar {etiqueta}.")
    try:
        return float(valor)
    except ValueError:
        raise ValueError(f"{etiqueta} debe ser un numero.")


def validar_rango(numero, minimo, maximo, etiqueta):
    """Verifica que un numero este dentro del rango permitido."""
    if numero < minimo or numero > maximo:
        raise ValueError(f"{etiqueta} debe estar entre {minimo} y {maximo}.")
    return numero


def calcular_promedio(notas):
    """Devuelve el promedio de una lista de notas, redondeado a 1 decimal."""
    return round(sum(notas) / len(notas), 1)


def obtener_estado(promedio, asistencia):
    """Aprueba solo si el promedio es >= 40 Y la asistencia es >= 75%."""
    if promedio >= NOTA_APROBACION and asistencia >= ASISTENCIA_MINIMA:
        return "APROBADO"
    return "REPROBADO"


def limpiar_nombre(valor, etiqueta):
    """Valida que el nombre no venga vacio y lo devuelve sin espacios sobrantes."""
    nombre = (valor or "").strip()
    if nombre == "":
        raise ValueError(f"Debes ingresar {etiqueta}.")
    return nombre


def contar_caracteres(nombre):
    """Cuenta las letras del nombre, sin considerar los espacios."""
    return len(nombre.replace(" ", ""))


def nombre_mas_largo(nombres):
    """Devuelve una tupla (nombre, cantidad de caracteres) del nombre mas largo."""
    ganador = max(nombres, key=contar_caracteres)
    return ganador, contar_caracteres(ganador)


# ---------------------------------------------------------------------------
# Rutas
# ---------------------------------------------------------------------------

@app.route("/")
def inicio():
    """Menu principal con los dos botones."""
    return render_template("index.html")


@app.route("/ejercicio1", methods=["GET", "POST"])
def ejercicio1():
    """Formulario de notas y asistencia."""
    resultado = None
    error = None
    datos = {"nota1": "", "nota2": "", "nota3": "", "asistencia": ""}

    if request.method == "POST":
        datos = {campo: request.form.get(campo, "") for campo in datos}
        try:
            notas = []
            for numero, campo in enumerate(["nota1", "nota2", "nota3"], start=1):
                nota = texto_a_numero(datos[campo], f"la nota {numero}")
                validar_rango(nota, NOTA_MINIMA, NOTA_MAXIMA, f"La nota {numero}")
                notas.append(nota)

            asistencia = texto_a_numero(datos["asistencia"], "la asistencia")
            validar_rango(asistencia, 0, 100, "La asistencia")

            promedio = calcular_promedio(notas)
            resultado = {
                "promedio": promedio,
                "asistencia": round(asistencia, 1),
                "estado": obtener_estado(promedio, asistencia),
            }
        except ValueError as e:
            error = str(e)

    return render_template(
        "ejercicio1.html", resultado=resultado, error=error, datos=datos
    )


@app.route("/ejercicio2", methods=["GET", "POST"])
def ejercicio2():
    """Formulario de los tres nombres."""
    resultado = None
    error = None
    datos = {"nombre1": "", "nombre2": "", "nombre3": ""}

    if request.method == "POST":
        datos = {campo: request.form.get(campo, "") for campo in datos}
        try:
            nombres = []
            for numero, campo in enumerate(["nombre1", "nombre2", "nombre3"], start=1):
                nombres.append(limpiar_nombre(datos[campo], f"el nombre {numero}"))

            if len(set(nombre.lower() for nombre in nombres)) < 3:
                raise ValueError("Los tres nombres deben ser diferentes.")

            ganador, cantidad = nombre_mas_largo(nombres)
            resultado = {"nombre": ganador, "cantidad": cantidad}
        except ValueError as e:
            error = str(e)

    return render_template(
        "ejercicio2.html", resultado=resultado, error=error, datos=datos
    )


if __name__ == "__main__":
    app.run(debug=True)