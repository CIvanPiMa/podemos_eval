import mysql.connector
import datetime
fecha_actual = datetime.datetime.now()


def actualiza_calendario():
    conn = mysql.connector.connect(
        host='localhost',
        user='eval',
        password='password',
        database='podemos_eval'
    )
    curs = conn.cursor()

    curs.execute("""
    SELECT id, fecha_pago
    FROM calendariopagos
    WHERE estatus != 'PAGADO' 
    """)
    lst_calendariopagos_id_fecha = curs.fetchall()

    for id, fecha in lst_calendariopagos_id_fecha:
        fecha_proximo = fecha + datetime.timedelta(days=7)
        if fecha_actual.date() > fecha_proximo:
            curs.execute("""
            UPDATE calendariopagos
            SET estatus = 'ATRASADO'
            WHERE id = {};
            """.format(id))
            conn.commit()


class Conexion:
    def __init__(self):
        conn = mysql.connector.connect(
            host='localhost',
            user='eval',
            password='password',
            database='podemos_eval'
        )
        self.curs = self.conn.cursor()

    def __del__(self):
        self.conn.close()


class Cliente(Conexion):

    def __init__(self):
        super().__init__()

    def __del__(self):
        super().__del__()

    def view(self):
        self.curs.execute("""
        SELECT * 
        FROM clientes
        """)
        clientes = self.curs.fetchall()
        return clientes

    def insert(self, id, nombre):
        self.curs.execute("""
        INSERT INTO clientes 
        VALUES ("{}", "{}");
        """.format(id, nombre))
        self.conn.commit()

    def edit(self, id, nombre):
        self.curs.execute("""
        UPDATE clientes
        SET nombre="{}"
        WHERE id="{}";
        """.format(nombre, id))
        self.conn.commit()


class Grupo(Conexion):

    def __init__(self):
        super().__init__()

    def __del__(self):
        super().__del__()

    def nombre_to_id(self, nombre):
        try:
            self.curs.execute("""
            SELECT id
            FROM grupos
            WHERE nombre = "{}"
            """.format(nombre))
            return self.curs.fetchone()[0]
        except TypeError:
            return ""

    def view(self):
        self.curs.execute("""
        SELECT nombre
        FROM grupos
        """)
        grupos = self.curs.fetchall()
        lst_grpuos = []
        for grupo in grupos:
            lst_grpuos.append(grupo[0])
        return lst_grpuos

    def add(self, grupo_id, cliente_id):
        self.curs.execute("""
        INSERT INTO miembros 
        VALUES ("{}", "{}");
        """.format(grupo_id, cliente_id))
        self.conn.commit()

    def remove(self, grupo_id, cliente_id):
        self.curs.execute("""
        DELETE FROM miembros
        WHERE grupo_id = "{}"
        AND cliente_id = "{}";
        """.format(grupo_id, cliente_id))
        self.conn.commit()

    def insert(self, id, nombre, clientes=[]):
        if clientes == []:
            raise mysql.connector.errors.IntegrityError

        self.curs.execute("""
        INSERT INTO grupos 
        VALUES ("{}", "{}");
        """.format(id, nombre))
        self.conn.commit()

        for cliente in clientes:
            self.curs.execute("""
            INSERT INTO miembros 
            VALUES ("{}", "{}");
            """.format(id, cliente))
            self.conn.commit()

    def members(self, nombre):
        self.curs.execute("""
        SELECT clientes.id, clientes.nombre
        FROM clientes
        JOIN miembros
        ON clientes.id = miembros.cliente_id
        JOIN grupos
        ON grupos.id = miembros.grupo_id
        WHERE grupos.nombre = "{}";
        """.format(nombre))
        miembros = self.curs.fetchall()
        return miembros

    def cuentas(self, nombre):
        self.curs.execute("""
        SELECT cuentas.id, estatus, monto, saldo
        FROM cuentas
        JOIN grupos
        ON cuentas.grupo_id = grupos.id
        WHERE grupos.nombre = "{}";
        """.format(nombre))
        cuentas = self.curs.fetchall()
        return cuentas

    def calendario(self, cuenta_id):
        self.curs.execute("""
        SELECT fecha_pago, num_pago, monto, estatus
        FROM calendariopagos
        WHERE cuenta_id = {};
        """.format(cuenta_id))
        registros = self.curs.fetchall()
        return registros

    def transacciones(self, cuenta_id):
        self.curs.execute("""
        SELECT fecha, num_pago, monto
        FROM transacciones
        WHERE cuenta_id={};
        """.format(cuenta_id))
        registros = self.curs.fetchall()
        return registros


class Cuenta(Conexion):
    def __init__(self):
        super().__init__()

    def __del__(self):
        super().__del__()

    def new(self, cuenta_id, grupo_id, monto, num_pagos):
        self.curs.execute("""
        INSERT INTO cuentas 
        VALUES ({0}, "{1}", 'DESEMBOLSADA', {2}, {2});
        """.format(cuenta_id, grupo_id, monto))
        self.conn.commit()

        monto_div = monto/num_pagos
        fecha_pago = fecha_actual
        for num_pago in range(1, num_pagos+1):
            fecha_pago += datetime.timedelta(days=7)
            fecha_pago.date()
            self.curs.execute("""
            INSERT INTO calendariopagos (cuenta_id, num_pago, monto, fecha_pago, estatus)
            VALUES ({}, {}, {}, "{}", 'PENDIENTE');
            """.format(cuenta_id, num_pago, monto_div, fecha_pago))
            self.conn.commit()

    def pago_pendiente(self, cuenta_id):
        self.curs.execute("""
            SELECT estatus
            FROM calendariopagos
            WHERE cuenta_id = {};
            """.format(cuenta_id))
        lst_calendario = self.curs.fetchall()

        num_pago = None
        estatus_pago = None

        for indx, estatus in enumerate(lst_calendario):
            if estatus[0] != "PAGADO":
                num_pago = indx + 1
                estatus_pago = estatus[0]
                break

        return num_pago, estatus_pago

    def ya_pagado(self, cuenta_id):
        ya_pagado = 0
        num_pago, estatus_pago = self.pago_pendiente(cuenta_id)

        if num_pago:
            self.curs.execute("""
                    SELECT monto
                    FROM transacciones
                    WHERE cuenta_id = {}
                    AND num_pago = {};
                    """.format(cuenta_id, num_pago))
            for pago in self.curs.fetchall():
                ya_pagado += pago[0]
        return ya_pagado

    def monto(self, cuenta_id):
        self.curs.execute("""
        SELECT monto 
        FROM calendariopagos
        WHERE cuenta_id = {}
        LIMIT 1;
        """.format(cuenta_id))
        return self.curs.fetchall()[0][0]

    def actualiza_cuenta(self, cuenta_id):
        num_pago, estatus_pago = self.pago_pendiente(cuenta_id)
        ya_pagado = self.ya_pagado(cuenta_id)

        self.curs.execute("""
        SELECT monto
        FROM calendariopagos
        WHERE cuenta_id = {}
        AND num_pago = {};
        """.format(cuenta_id, num_pago))
        monto = self.curs.fetchall()[0][0]

        pendiente = monto - ya_pagado

        if pendiente == 0:
            self.curs.execute("""
            UPDATE calendariopagos
            SET estatus = 'PAGADO'
            WHERE cuenta_id = {}
            AND num_pago = {};
            """.format(cuenta_id, num_pago))
            self.conn.commit()

        elif estatus_pago == 'PENDIENTE' and ya_pagado > 0:
            self.curs.execute("""
            UPDATE calendariopagos
            SET estatus = 'PARCIAL'
            WHERE cuenta_id = {}
            AND num_pago = {};
            """.format(cuenta_id, num_pago))
            self.conn.commit()

    def pago(self, cuenta_id, pago):
        if pago == 0:
            return 3, 'No se pueden realizar pagos de $0'

        num_pago, estatus_numpago = self.pago_pendiente(cuenta_id)

        self.curs.execute("""
        SELECT estatus, saldo
        FROM cuentas
        where id = {};
        """.format(cuenta_id))
        estatus, saldo = self.curs.fetchall()[0]

        if estatus == 'CERRADA':
            return 3, 'La cuenta "{}", ya esta cerrada y no se pueden realizar pagos'.format(cuenta_id)

        pago_maximo = self.monto(cuenta_id) - self.ya_pagado(cuenta_id)

        if pago > pago_maximo:
            return 2, 'El pago excede el limite de ${}'.format(pago_maximo)

        self.curs.execute("""
        INSERT INTO transacciones (cuenta_id, num_pago, fecha, monto)
        VALUES ({}, {}, "{}", {});
        """.format(cuenta_id, num_pago, fecha_actual, pago))

        saldo -= pago
        mensaje = "El pago se realizó con éxito"
        num = 1

        if saldo == 0:
            self.curs.execute("""
            UPDATE cuentas
            SET estatus = 'CERRADA'
            WHERE id = {};
            """.format(cuenta_id))
            mensaje += ', la cuenta "{}" se a cerrado'.format(cuenta_id)

        self.curs.execute("""
        UPDATE cuentas
        SET saldo = {}
        WHERE id = {};
        """.format(saldo, cuenta_id))
        self.conn.commit()
        return num, mensaje
