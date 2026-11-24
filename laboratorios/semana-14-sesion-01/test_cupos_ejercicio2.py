"""Pruebas del Ejercicio 2. La primera ya esta escrita. Escribe las demas
una a la vez, en este orden, y antes de cada una haz pasar la anterior:

1. Un estudiante sin reservas puede reservar.
2. Con 2 reservas en la semana, todavia puede.
3. Con 3 reservas en la semana, ya no puede.
4. Las reservas de otra semana no cuentan (2026-11-16 y 2026-11-23 son
   lunes de semanas distintas; 2026-11-22 es el domingo de la semana del 16).
5. Cancelar una reserva libera su lugar.
6. Un equipo oficial puede tener 6 reservas en la semana, pero no 7.
7. Registrar la cuarta reserva lanza ValueError (usa pytest.raises), y
   despues de intentarlo el estudiante sigue con 3.

Anota en la bitacora del README, por cada prueba: con que mensaje fallo,
que cambiaste para que pase, y que refactorizaste.
"""

from cupos_ejercicio2 import CupoSemanal
import pytest


def test_sin_reservas_puede_reservar():
    cupo = CupoSemanal()
    assert cupo.puede_reservar("ana", "2026-11-16")


def test_con_dos_reservas_todavia_puede():
    cupo = CupoSemanal()
    for i in range(2):
        cupo.registrar(str(i), "ana", "2026-11-16")
    assert cupo.puede_reservar("ana", "2026-11-22")


def test_con_tres_reservas_no_puede():
    cupo = CupoSemanal()
    for i in range(3):
        cupo.registrar(str(i), "ana", "2026-11-16")
    assert not cupo.puede_reservar("ana", "2026-11-22")


def test_las_otras_semanas_no_cuentan():
    cupo = CupoSemanal()
    for i in range(3):
        cupo.registrar(str(i), "ana", "2026-11-16")
    assert not cupo.puede_reservar("ana", "2026-11-22")
    assert cupo.puede_reservar("ana", "2026-11-23")


def test_cancelar_libera_un_lugar():
    cupo = CupoSemanal()
    for i in range(3):
        cupo.registrar(str(i), "ana", "2026-11-16")
    cupo.cancelar("1")
    assert cupo.puede_reservar("ana", "2026-11-16")


def test_equipo_oficial_puede_registrar_seis():
    cupo = CupoSemanal()
    cupo.registrar_equipo_oficial("equipo")
    for i in range(6):
        assert cupo.puede_reservar("equipo", "2026-11-16")
        cupo.registrar(str(i), "equipo", "2026-11-16")
    assert not cupo.puede_reservar("equipo", "2026-11-16")
    with pytest.raises(ValueError, match="cupo semanal agotado"):
        cupo.registrar("6", "equipo", "2026-11-16")


def test_cuarta_reserva_no_se_registra():
    cupo = CupoSemanal()
    for i in range(3):
        cupo.registrar(str(i), "ana", "2026-11-16")
    with pytest.raises(ValueError, match="cupo semanal agotado"):
        cupo.registrar("3", "ana", "2026-11-16")
    with pytest.raises(ValueError):
        cupo.cancelar("3")
    cupo.cancelar("0")
    assert cupo.puede_reservar("ana", "2026-11-16")
