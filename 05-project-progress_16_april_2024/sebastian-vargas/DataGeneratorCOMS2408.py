from datetime import datetime, timedelta
import random
import matplotlib.pyplot as plt

import random

def asignar_valor_aleatorio():
    # Lista de valores posibles
    valores_posibles = [5, 3.3]
    
    # Asignar aleatoriamente un valor de la lista
    valor_asignado_Vop = random.choice(valores_posibles)
    
    return valor_asignado_Vop


#Parametros Antenas
potencia_COMS2408TX = 25 #En Watts
Vop_COMS2408TX = asignar_valor_aleatorio() #En Volts
corriente_COMS2408TX = (potencia_COMS2408TX / Vop_COMS2408TX) 
ciclos_de_trabajo = 15
tiempo_completo = 24
cilcos_de_trabajo_horas = ((ciclos_de_trabajo * tiempo_completo)/100)

def generar_hora_inicio_aleatoria():
    # Generar una hora aleatoria entre las 00:00 y las 23:59
    hora = random.randint(0, 23)
    minutos = random.randint(0, 59)
    segundos = random.randint(0, 59)
    return hora, minutos, segundos

def generar_tiempo_aleatorio():
    # Generar minutos aleatorios entre 0 y 59 
    minutos = random.randint(0, 59)
    # Generar segundos aleatorios entre 0 y 59
    segundos = random.randint(0, 59)
    return minutos, segundos

def formato_tiempo(minutos, segundos):
    return "{:02d}:{:02d}".format(minutos, segundos)

# Función para convertir tiempo a timedelta
def tiempo_a_timedelta(minutos, segundos):
    return timedelta(minutes=minutos, seconds=segundos)

def generar_lista_horas_y_tiempos(num_elementos, fecha):
    lista_horas_tiempos = []
    tiempo_total = timedelta()
    while tiempo_total.total_seconds() < 3.6 * 3600 and len(lista_horas_tiempos) < num_elementos:
        hora_inicio = generar_hora_inicio_aleatoria()
        minutos, segundos = generar_tiempo_aleatorio()
        tiempo = tiempo_a_timedelta(minutos, segundos)
        if tiempo_total + tiempo <= timedelta(hours=3, minutes=36):
            lista_horas_tiempos.append((fecha, hora_inicio, tiempo))
            tiempo_total += tiempo
    return lista_horas_tiempos

# Número de elementos en la lista que deseas generar
num_elementos = 10

# Crear una lista para almacenar los próximos 14 días
lista_14_dias = []

# Obtener la fecha actual
fecha_actual = datetime.now().date()

# Iterar sobre los próximos 14 días y agregarlos a la lista
for i in range(14):
    fecha = fecha_actual + timedelta(days=i)
    lista_14_dias.append(fecha)

# Generar la lista de horas de inicio y tiempos aleatorios para cada día
for fecha in lista_14_dias:
    lista_horas_tiempos = generar_lista_horas_y_tiempos(num_elementos, fecha)
    
    # Imprimir la lista de fechas, horas de inicio y tiempos
    print("Lista de horas de inicio y tiempos aleatorios con una suma total menor a 3.6 horas para la fecha:", fecha)
    for i, (fecha, hora_inicio, tiempo) in enumerate(lista_horas_tiempos, 1):
        corriente_mAs = tiempo.seconds * corriente_COMS2408TX
        print("Elemento {}: Fecha: {}, Hora de inicio: {}, Tiempo: {}, Corriente: {} mAs".format(i, fecha.strftime("%Y-%m-%d"),
                                                                                                formato_tiempo(hora_inicio[0], hora_inicio[1]),
                                                                                                formato_tiempo(tiempo.seconds // 60, tiempo.seconds % 60),
                                                                                                corriente_mAs))



