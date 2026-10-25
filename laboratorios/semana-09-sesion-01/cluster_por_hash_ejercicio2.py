"""Ejercicio 2: sharding por hash del estudiante, consulta dirigida y
scatter-gather.

Corre las pruebas con:

    pytest test_cluster_por_hash_ejercicio2.py

No cambies los nombres de la clase ni de los metodos: los tests
dependen de que existan exactamente asi.
"""

from datos_reservas import hash_estable


class ClusterPorHash:
    def __init__(self, cantidad_de_shards):
        self.cantidad_de_shards = cantidad_de_shards
        self.shards = []
        for _ in range(cantidad_de_shards):
            self.shards.append([])

    def shard_de(self, id_estudiante):
        # TODO: devuelve el shard (0 a cantidad_de_shards - 1) de este
        # estudiante: el hash estable de su id, modulo la cantidad de
        # shards.
        return hash_estable(id_estudiante) % self.cantidad_de_shards

    def insertar(self, reserva):
        # TODO: agrega la reserva a la lista del shard que le corresponde
        # segun su id_estudiante.
        shard = self.shard_de(reserva.id_estudiante)
        self.shards[shard].append(reserva)

    def tamanos(self):
        # TODO: devuelve una lista con cuantas reservas tiene cada shard.
        conteo = []

        for shard in self.shards:
            conteo.append(len(shard))

        return conteo

    def reservas_de_estudiante(self, id_estudiante):
        # TODO: consulta dirigida. Devuelve una tupla
        # (reservas_encontradas, shards_consultados), revisando solo el
        # shard donde viven las reservas de ese estudiante.
        reservas = []

        shard = self.shard_de(id_estudiante)

        for reservation in self.shards[shard]:
            if reservation.id_estudiante == id_estudiante:
                reservas.append(reservation)
        
        return reservas, 1

    def reservas_de_cancha(self, campus, cancha, fecha):
        # TODO: devuelve una tupla (reservas_encontradas,
        # shards_consultados) con todas las reservas de esa cancha, de ese
        # campus, en esa fecha. Piensa primero en cuantos shards tienes
        # que revisar para no perder ninguna.

        reservas = []

        for shard in self.shards:
            for reservation in shard:
                if reservation.campus == campus and reservation.cancha == cancha and reservation.fecha == fecha:
                    reservas.append(reservas)

        return reservas, self.cantidad_de_shards


def fraccion_que_cambia_de_shard(claves, shards_antes, shards_despues):
    # TODO: devuelve que fraccion de las claves (entre 0 y 1) cae en un
    # shard distinto al pasar de "shards_antes" a "shards_despues" shards
    # con este mismo reparto por hash y modulo.
    conteo_cambio = 0

    for clave in claves:
        if hash_estable(clave) % shards_antes != hash_estable(clave) % shards_despues:
            conteo_cambio += 1

    return conteo_cambio / len(claves) 
