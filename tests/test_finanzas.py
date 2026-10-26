import pytest

from app import finanzas


def test_cuota_10_millones_36_meses_12_porciento():
    assert finanzas.cuota_credito(10_000_000, 12, 36) == pytest.approx(332_143, abs=1)


def test_cuota_12_meses():
    assert finanzas.cuota_credito(1_000_000, 12, 12) == 88848.79


def test_cuota_tasa_cero():
    assert finanzas.cuota_credito(1200, 0, 12) == 100


def test_total_e_intereses():
    total, intereses = finanzas.total_e_intereses(10_000_000, 12, 36)
    assert total == pytest.approx(332_143.06 * 36, abs=40)
    assert intereses == pytest.approx(total - 10_000_000)


def test_ahorro_mensual():
    assert finanzas.ahorro_mensual(1200, 12) == 100


def test_interes_compuesto():
    assert finanzas.interes_compuesto(1000, 12, 1) == 1126.83


@pytest.mark.parametrize("f,args", [
    (finanzas.cuota_credito, (-1, 5, 12)),
    (finanzas.cuota_credito, (1000, 5, 0)),
    (finanzas.ahorro_mensual, (100, 0)),
    (finanzas.interes_compuesto, (0, 5, 1)),
])
def test_entradas_invalidas(f, args):
    with pytest.raises(ValueError):
        f(*args)
