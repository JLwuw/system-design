"""Pruebas del Ejercicio 3: las escriben ustedes, en pareja, una a la vez."""

import pytest

from recurrentes_ejercicio3 import AgendaDeCancha


def test_calendario_se_reutiliza_por_fecha():
    agenda = AgendaDeCancha("cancha-1")
    assert agenda.calendario("2026-11-16") is agenda.calendario("2026-11-16")
    assert agenda.calendario("2026-11-16") is not agenda.calendario("2026-11-23")


def test_reserva_cada_semana_con_fechas_e_ids():
    agenda = AgendaDeCancha("cancha-1")
    assert agenda.reservar_cada_semana("entreno", "ana", "2026-12-28", 18, 19, 3) == [
        ("2026-12-28", "reservada"), ("2027-01-04", "reservada"),
        ("2027-01-11", "reservada")]
    for i, fecha in enumerate(("2026-12-28", "2027-01-04", "2027-01-11"), 1):
        assert agenda.calendario(fecha).franja_de(f"entreno-{i}").inicio == 18


def test_salta_franja_ocupada_y_continua():
    agenda = AgendaDeCancha("cancha-1")
    agenda.calendario("2026-11-23").reservar("otra", "beto", 18, 19)
    assert agenda.reservar_cada_semana("entreno", "ana", "2026-11-16", 18, 19, 3) == [
        ("2026-11-16", "reservada"), ("2026-11-23", "ocupada"),
        ("2026-11-30", "reservada")]
    assert agenda.calendario("2026-11-30").franja_de("entreno-3").fin == 19


def test_limite_por_dia_no_impide_las_otras_semanas():
    agenda = AgendaDeCancha("cancha-1")
    calendario = agenda.calendario("2026-11-23")
    calendario.reservar("otra", "ana", 8, 10)
    assert agenda.reservar_cada_semana("entreno", "ana", "2026-11-16", 18, 19, 2) == [
        ("2026-11-16", "reservada"), ("2026-11-23", "limite")]
    assert len(calendario.reservas()) == 1


def test_ocupacion_tiene_prioridad_sobre_limite():
    agenda = AgendaDeCancha("cancha-1")
    calendario = agenda.calendario("2026-11-16")
    calendario.reservar("ana", "ana", 8, 10)
    calendario.reservar("beto", "beto", 18, 19)
    assert agenda.reservar_cada_semana("x", "ana", "2026-11-16", 18, 19, 1) == [
        ("2026-11-16", "ocupada")]


@pytest.mark.parametrize("semanas", [0, -1, 13])
def test_semanas_invalidas_no_reservan(semanas):
    agenda = AgendaDeCancha("cancha-1")
    with pytest.raises(ValueError):
        agenda.reservar_cada_semana("x", "ana", "2026-11-16", 18, 19, semanas)
    assert agenda.calendario("2026-11-16").reservas() == []


def test_doce_semanas_es_valido():
    agenda = AgendaDeCancha("cancha-1")
    assert len(agenda.reservar_cada_semana("x", "ana", "2026-11-16", 18, 19, 12)) == 12
