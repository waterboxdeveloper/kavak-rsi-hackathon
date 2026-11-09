"""Constantes compartidas por el generador de casos, los agentes y el scorer.

Todo lo que necesite ser *deterministico* vive aqui. Si el generador y el
agente usaran tipos de cambio distintos, el benchmark dejaria de ser confiable.
"""

# Tipo de cambio fijo del benchmark. No consultamos APIs: queremos que el
# resultado de hoy sea identico al de manana.
USD_MXN = 18.50

# Factor de conversion millas -> kilometros.
MILES_TO_KM = 1.60934

# Catalogo de modelos con el rango de anos en que existio esa generacion.
# Sirve para dos cosas: generar casos validos y detectar ano imposible.
MODELS = [
    ("Volkswagen", "Jetta", (2011, 2018)),
    ("Nissan", "Versa", (2012, 2019)),
    ("Chevrolet", "Aveo", (2012, 2017)),
    ("Kia", "Rio", (2016, 2022)),
    ("Mazda", "Mazda3", (2014, 2018)),
    ("Toyota", "Corolla", (2014, 2019)),
    ("Honda", "City", (2015, 2020)),
    ("Hyundai", "Grand i10", (2016, 2022)),
]

MODEL_YEARS = {(mk, md): yrs for mk, md, yrs in MODELS}

# Campos que el scorer compara campo a campo.
SCORED_FIELDS = ["make", "model", "year", "odometer_km", "price_mxn", "vin", "flags"]

# Banderas de riesgo que el sistema puede emitir.
FLAGS = ["salvage", "vin_invalid", "year_model_mismatch", "duplicate"]
