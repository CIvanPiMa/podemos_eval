import unittest
from back import Cliente, Grupo, Cuenta, actualiza_calendario


class TestCliente(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.obj_cliente = Cliente()

    def test_view(self):
        result = [('ABCDE03', 'IRMA MARQUEZ RUBIO'), ('ASDFG08', 'SANDRA SANCHEZ GONZALEZ'), ('HJKLL09', 'ANGELA GOMEZ MONROY'), ('MNOPQ01', 'GERTRUDIS LOPEZ MARTINEZ'), ('NMZXC11', 'DANIELA HERNANDEZ GUERRERO'), ('OPQRS04', 'ALEIDA SANCHEZ AMOR'), ('QRSTU02', 'FERNANDA JUAREZ LOPEZ'), ('QWERT06', 'ALBA PEREZ TORRES'), ('TYUIQ05', 'LORENA GARCIA ROCHA'), ('YUIOP07', 'ELISEO CHAVEZ OLVERA'), ('ZXCVB10', 'KARLA ENRIQUEZ NAVARRETE')]
        self.assertEqual(self.obj_cliente.view(), result)


class TestGrupo(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.obj_grupo = Grupo()

    def test_nombre_to_id(self):
        result = "ABCD2"
        self.assertEqual(self.obj_grupo.nombre_to_id("CHARLIE'S ANGELS"), result)

    def test_view(self):
        result = ["CHARLIE'S ANGELS", 'KITTIE', 'POWERPUFF GIRLS']
        self.assertEqual(self.obj_grupo.view(), result)

    def test_members(self):
        result = [('ASDFG08', 'SANDRA SANCHEZ GONZALEZ'), ('QWERT06', 'ALBA PEREZ TORRES'), ('TYUIQ05', 'LORENA GARCIA ROCHA'), ('YUIOP07', 'ELISEO CHAVEZ OLVERA')]
        self.assertEqual(self.obj_grupo.members("CHARLIE'S ANGELS"), result)

    # def test_cuentas(self):
    #     result = [('12345', 'DESEMBOLSADA', Decimal('75000.00'), Decimal('64500.00'))]
    #     self.assertEqual(self.obj_grupo.cuentas("CHARLIE'S ANGELS"), result)

    # def test_calendario(self):
    #     result = [(datetime.date(2018, 12, 7), 1, Decimal('37500.00'), 'PAGADO'), (datetime.date(2018, 12, 14), 2, Decimal('37500.00'), 'PAGADO'), (datetime.date(2018, 12, 21), 3, Decimal('37500.00'), 'ATRASADO'), (datetime.date(2018, 12, 28), 4, Decimal('37500.00'), 'ATRASADO')]
    #     self.assertEqual(self.obj_grupo.calendario(10001), result)

    # def test_transacciones(self):
    #     result = [(datetime.datetime(2007, 12, 18, 11, 34), 1, Decimal('37500.00')), (datetime.datetime(2007, 12, 18, 10, 4), 2, Decimal('37500.00')), (datetime.datetime(2007, 12, 18, 18, 50), 3, Decimal('-30000.00')), (datetime.datetime(2007, 12, 18, 18, 51), 3, Decimal('-7500.00')), (datetime.datetime(2014, 12, 18, 9, 59), 3, Decimal('37500.00')), (datetime.datetime(2021, 12, 18, 11, 5), 3, Decimal('500.00'))]
    #     self.assertEqual(self.obj_grupo.transacciones(10001), result)


class TestCuenta(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.obj_cuenta = Cuenta()

    def test_pago_pendiente(self):
        result = (3, 'ATRASADO')
        self.assertEqual(self.obj_cuenta.pago_pendiente(10001), result)

    def test_ya_pagado(self):
        result = 500.00
        self.assertEqual(self.obj_cuenta.ya_pagado(10001), result)

    def test_monto(self):
        result = 37500.00
        self.assertEqual(self.obj_cuenta.monto(10001), result)

    def test_pago(self):
        result = (3, 'No se pueden realizar pagos de $0')
        self.assertEqual(self.obj_cuenta.pago(10001, 0), result)
        result = (3, 'La cuenta "23001", ya esta cerrada y no se pueden realizar pagos')
        self.assertEqual(self.obj_cuenta.pago(23001, 10), result)
        result = (2, 'El pago excede el limite de $37000.00')
        self.assertEqual(self.obj_cuenta.pago(10001, 1000000), result)
        # result = (1, 'El pago se realizó con éxito')
        # self.assertEqual(self.obj_cuenta.pago(10001, 100), result)


if __name__ == '__main__':
    unittest.main()
