"""Ejercicio 2: balanceador round robin con health check.

Corre las pruebas con:

    pytest test_balanceador_ejercicio2.py

No cambies los nombres de la clase ni de los metodos: los tests
dependen de que existan exactamente asi.
"""


class BalanceadorRoundRobin:
    def __init__(self, servidores):
        self.servidores = servidores
        self.siguiente = 0

    def enviar(self, duracion):
        # TODO: reparte las solicitudes en turnos: la primera al servidor
        # en la posicion self.siguiente, la proxima al que sigue, y al
        # llegar al final de la lista, vuelve al primero (el operador %
        # resuelve la vuelta).
        #
        # Antes de enviarle una solicitud a un servidor, consulta su
        # health_check(). Si no esta sano, o si atender(duracion)
        # devuelve False porque esta lleno, prueba con el siguiente de la
        # lista, sin pasar dos veces por el mismo servidor.
        #
        # Si un servidor acepto la solicitud, deja self.siguiente apuntando
        # al servidor que viene despues de el y devuelve servidor.nombre.
        # Si ninguno la acepto, devuelve None.

        cantidad_servidores = len(self.servidores)

        for _ in range(cantidad_servidores):
            servidor = self.servidores[self.siguiente]
            
            if not servidor.health_check() or not servidor.puede_atender():
                self.siguiente = (self.siguiente + 1) % cantidad_servidores
                continue
            
            servidor.atender(duracion)
            self.siguiente = (self.siguiente + 1) % cantidad_servidores
            return servidor.nombre


        return None
