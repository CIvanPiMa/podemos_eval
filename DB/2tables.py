import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='eval',
    password='password',
    database='podemos_eval'
)
curs = conn.cursor()

curs.execute("""
    CREATE TABLE IF NOT EXISTS `Grupos` (
    `id` VARCHAR(5) NOT NULL COMMENT '',
    `nombre` VARCHAR(20) NOT NULL UNIQUE COMMENT '',
    PRIMARY KEY (`id`)  COMMENT '')
    ENGINE = InnoDB
    DEFAULT CHARACTER SET = utf8;
    """)
print('Tabla "Grupos" creada')

curs.execute("""
    CREATE TABLE IF NOT EXISTS `Cuentas` (
    `id` VARCHAR(5) NOT NULL COMMENT '',
    `grupo_id` VARCHAR(5) NOT NULL COMMENT '',
    `estatus` VARCHAR(15) NOT NULL COMMENT '',
    `monto` DECIMAL(15,2) NOT NULL COMMENT '',
    `saldo` DECIMAL(15,2) NOT NULL COMMENT '',
    PRIMARY KEY (`id`)  COMMENT '',
    INDEX `fk_grupo_idx` (`grupo_id` ASC)  COMMENT '',
    CONSTRAINT `fk_Cuentas_1`
    FOREIGN KEY (`grupo_id`)
    REFERENCES `Grupos` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
    ENGINE = InnoDB
    DEFAULT CHARACTER SET = utf8;
    """)
print('Tabla "Cuentas" creada')

curs.execute("""
    CREATE TABLE IF NOT EXISTS `CalendarioPagos` (
    `id` INT(11) NOT NULL AUTO_INCREMENT COMMENT '',
    `cuenta_id` VARCHAR(5) NOT NULL COMMENT '',
    `num_pago` INT(11) NOT NULL COMMENT '',
    `monto` DECIMAL(15,2) NOT NULL COMMENT '',
    `fecha_pago` DATE NOT NULL COMMENT '',
    `estatus` VARCHAR(15) NOT NULL COMMENT '',
    PRIMARY KEY (`id`)  COMMENT '',
    INDEX `fk_CalendarioPagos_1_idx` (`cuenta_id` ASC)  COMMENT '',
    CONSTRAINT `fk_CalendarioPagos_1`
    FOREIGN KEY (`cuenta_id`)
    REFERENCES `Cuentas` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
    ENGINE = InnoDB
    DEFAULT CHARACTER SET = utf8;
    """)
print('Tabla "CalendarioPagos" creada')

curs.execute("""
    CREATE TABLE IF NOT EXISTS `Clientes` (
    `id` VARCHAR(7) NOT NULL COMMENT '',
    `nombre` VARCHAR(60) NOT NULL COMMENT '',
    PRIMARY KEY (`id`)  COMMENT '')
    ENGINE = InnoDB
    DEFAULT CHARACTER SET = utf8;
    """)
print('Tabla "Clientes" creada')

curs.execute("""
    CREATE TABLE IF NOT EXISTS `Miembros` (
    `grupo_id` VARCHAR(5) NOT NULL COMMENT '',
    `cliente_id` VARCHAR(7) NOT NULL COMMENT '',
    PRIMARY KEY (`grupo_id`, `cliente_id`)  COMMENT '',
    INDEX `fk_cliente_idx` (`cliente_id` ASC)  COMMENT '',
    CONSTRAINT `fk_cliente`
    FOREIGN KEY (`cliente_id`)
    REFERENCES `Clientes` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
    CONSTRAINT `fk_grupo`
    FOREIGN KEY (`grupo_id`)
    REFERENCES `Grupos` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
    ENGINE = InnoDB
    DEFAULT CHARACTER SET = utf8;
    """)
print('Tabla "Miembros" creada')

curs.execute("""
    CREATE TABLE IF NOT EXISTS `Transacciones` (
    `id` INT(11) NOT NULL AUTO_INCREMENT COMMENT '',
    `cuenta_id` VARCHAR(5) NOT NULL COMMENT '',
    `num_pago` INT(11) NOT NULL COMMENT '',
    `fecha` DATETIME NOT NULL COMMENT '',
    `monto` DECIMAL(15,2) NOT NULL COMMENT '',
    PRIMARY KEY (`id`)  COMMENT '',
    INDEX `fk_Transacciones_1_idx` (`cuenta_id` ASC)  COMMENT '',
    CONSTRAINT `fk_Transacciones_1`
    FOREIGN KEY (`cuenta_id`)
    REFERENCES `Cuentas` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
    ENGINE = InnoDB
    DEFAULT CHARACTER SET = utf8;
    """)
print('Tabla "Transacciones" creada')
