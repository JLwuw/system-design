"""Ejercicio 1: la misma cobertura, en la base de la piramide. Empieza
vacio: se escribe en vivo.

Por cada prueba de punta a punta de test_suite_heredada.py que se pueda
bajar de nivel, una prueba unitaria del servicio (con RepositorioEnMemoria)
o una de integracion (con RepositorioSQLite o con la API), y una sola
prueba de punta a punta que recorra el camino completo.

    pytest test_rapidas_ejercicio1.py --durations=0
"""

# fixture: todos los componentes para que el ambiente de testing este functional

import pytest
from repositorio import RepositorioEnMemoria, RepositorioSQLite
from servicio import ServicioDeReservas
from api import ApiDeReservas
from entorno_e2e import NavegadorSimulado

@pytest.fixture
def servicio():
    return ServicioDeReservas(repositorio=RepositorioEnMemoria)


def test_cuarta_reserva_rechazada(servicio):
    servicio.reservar("r1", "pedro", "2026-11-26")
    servicio.reservar("r2", "pedro", "2026-11-26")
    servicio.reservar("r3", "pedro", "2026-11-26")
    
    assert servicio.motivo_de_rechazo("pedro", "2026-11-26") == "cupo semanal agotado"

    with pytest.raises(ValueError, match="cupo semanal agotado"):
        servicio.reservar("r4", "pedro", "2026-11-26")

def test_cuarta_reserva_semana_diferente_acepta(servicio):
    servicio.reservar("r1", "pedro", "2026-11-26")
    servicio.reservar("r2", "pedro", "2026-11-26")
    servicio.reservar("r3", "pedro", "2026-11-26")

    servicio.reservar("r4", "pedro", "2026-21-26")


def test_api_cancelar_reserva_desconocida_404():
    servicio_sql = RepositorioSQLite(":memory:")
    api = ApiDeReservas(servicio_sql)

    respuesta = api.manejar({
        "metodo": "DELETE",
        "ruta": "/ruta/desconocida",
        "reserva": "r1"
    })

    assert respuesta["estado"] == 404


def test_reservar_cancelar_ver_puntos():
    navegador = NavegadorSimulado()

    navegador.iniciar_sesion("pedro")
    assert navegador.reservar("r1", "2026-11-26")["estado"] == 201
    assert navegador.cancelar("r1", 30)["estado"] == 200
    assert navegador.ver_puntos() == 2