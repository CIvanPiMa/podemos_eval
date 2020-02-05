from tkinter import *
from tkinter import messagebox
from back import *

obj_cliente = Cliente()
obj_grupo = Grupo()
obj_cuenta = Cuenta()
lst_grupos = obj_grupo.view()


##################################################
# Ventana clientes
##################################################
def clientes_pop():
    v2 = Toplevel()
    v2.title('Clientes')
    v2.iconbitmap('img/podemos.ico')
    v2.geometry('430x280')

    # ---------- Funciones ----------

    def muestra_usuarios():
        box_v2.delete(0, END)
        for cliente in obj_cliente.view():
            box_v2.insert(END, cliente[0] + ' - ' + cliente[1])

    def selecciona_usuario(event):
        try:
            global usuario
            box_v2.curselection()
            ind = box_v2.curselection()[0]
            usuario = box_v2.get(ind)
            id, nombre = usuario.split(' - ')
            ent_id.delete(0, END)
            ent_nombre.delete(0, END)
            ent_id.insert(END, id)
            global id_original
            id_original = ent_id.get()
            ent_nombre.insert(END, nombre)
        except IndexError:
            pass

    def btn_v2_nuevo_f():
        try:
            id = ent_id.get()
            nombre = ent_nombre.get()
            if id.replace(" ", "") == "" or nombre.replace(" ", "") == "":
                messagebox.showerror('Crear Cliente', 'Ingrese un nombre y una ID al cliente')
            else:
                obj_cliente.insert(id, nombre)
                messagebox.showinfo('Crear Cliente', 'Cliente {}, con id {}, a sido creado'.format(nombre, id))
                ent_id.delete(0, END)
                ent_nombre.delete(0, END)
                muestra_usuarios()
        except mysql.connector.errors.IntegrityError:
            messagebox.showerror('Crear Cliente', 'Se ingresaron datos incorrectos, intentelo nuevamente')

    def btn_v2_editar_f():
        id = ent_id.get()
        nombre = ent_nombre.get()
        if id.replace(" ", "") == "" or nombre.replace(" ", "") == "":
            messagebox.showwarning('Editar Cliente', 'Seleccione el cliente que desea editar')
        else:
            if id_original != id:
                messagebox.showerror('Editar Cliente', 'El ID NO puede ser modificado')
                ent_id.delete(0, END)
                ent_id.insert(END, id_original)
            else:
                obj_cliente.edit(id, nombre)
                ent_id.delete(0, END)
                ent_nombre.delete(0, END)
                messagebox.showinfo('Editar Cliente', 'Cliente {}, con id {}, a sido editado'.format(nombre, id))
                muestra_usuarios()

    # ---------- Widgets ----------

    btn_v2_nuevo = Button(v2, text='Nuevo', width=15, command=btn_v2_nuevo_f)
    btn_v2_nuevo.grid(row=0, column=1, padx=10, pady=5)
    btn_v2_editar = Button(v2, text='Editar', width=15, command=btn_v2_editar_f)
    btn_v2_editar.grid(row=1, column=1, padx=10, pady=5)

    box_v2 = Listbox(v2, width=40, height=10)
    box_v2.grid(row=0, column=2, rowspan=4, padx=10, pady=5)
    box_v2.bind('<<ListboxSelect>>', selecciona_usuario)

    lbl_id = Label(v2, text='ID (inmutable)')
    lbl_id.grid(row=5, column=1, padx=10, pady=5)
    ent_id = Entry(v2, width=40)
    ent_id.grid(row=5, column=2, padx=10, pady=5)

    lbl_nombre = Label(v2, text='Nombre')
    lbl_nombre.grid(row=6, column=1, padx=10, pady=5)
    ent_nombre = Entry(v2, width=40)
    ent_nombre.grid(row=6, column=2, padx=10, pady=5)

    muestra_usuarios()


##################################################
# Ventana grupos
##################################################
def grupos_pop():
    v3 = Toplevel()
    v3.title('Grupos')
    v3.iconbitmap('img/podemos.ico')
    v3.geometry('430x280')

    # ---------- Funciones ----------
    def btn_v3_buscar_f():
        if drp_grupo.get() == 'Grupos':
            messagebox.showwarning('Buscar Grupo', 'Seleccione un grupo para ver sus miembros')
        else:
            box_v3.delete(0, END)
            ent_grupoid.delete(0, END)
            ent_gruponombre.delete(0, END)

            for miembro in obj_grupo.members(drp_grupo.get()):
                box_v3.insert(END, miembro[0] + ' - ' + miembro[1])

            ent_gruponombre.insert(END, drp_grupo.get())
            ent_grupoid.insert(END, obj_grupo.nombre_to_id(drp_grupo.get()))

    def btn_v3_nuevo_f():
        id = ent_grupoid.get()
        nombre = ent_gruponombre.get()
        if id.replace(" ", "") == "" or nombre.replace(" ", "") == "":
            messagebox.showwarning('Grupo nuevo', 'agregue un ID y un nobre para crear el grupo')
        else:
            clientes = []
            #################################################################################
            v2 = Toplevel()
            v2.title('Agregar clientes')
            v2.iconbitmap('img/podemos.ico')
            v2.geometry('430x280')

            # ---------- Funciones ----------

            def selecciona_usuario(event):
                try:
                    global usuario
                    box_v2.curselection()
                    ind = box_v2.curselection()[0]
                    usuario = box_v2.get(ind)
                    id, nombre = usuario.split(' - ')
                    ent_id.delete(0, END)
                    ent_id.insert(END, id)
                except IndexError:
                    pass

            def btn_v2_añadir_f():
                id = ent_id.get(0)
                if id in clientes:
                    messagebox.showwarning('Creación de grupos', 'El cliente ya fue seleccionado para el grupo')
                elif id.replace(" ", "") == "":
                    messagebox.showwarning('Creación de grupos', 'Elija el cliente para el grupo')
                else:
                    clientes.append(id)
                ent_id.delete(0, END)

            def btn_v2_aplicar_f():
                try:
                    obj_grupo.insert(id, nombre, clientes)
                    messagebox.showinfo('NUEVO Grupo', 'Grupo {}, con id {}, a sido creado'.format(nombre, id))
                    v2.destroy()
                except:
                    messagebox.showerror('NUEVO Grupo', 'Se ingresaron datos incorrectos, intentelo nuevamente')
                    v2.destroy()

            # ---------- Widgets ----------

            btn_v2_nuevo = Button(v2, text='Añadir', width=15, command=btn_v2_añadir_f)
            btn_v2_nuevo.grid(row=0, column=1, padx=10, pady=5)
            btn_v2_editar = Button(v2, text='Crear', width=15, command=btn_v2_aplicar_f)
            btn_v2_editar.grid(row=1, column=1, padx=10, pady=5)

            box_v2 = Listbox(v2, width=40, height=10)
            box_v2.grid(row=0, column=2, rowspan=4, padx=10, pady=5)
            box_v2.bind('<<ListboxSelect>>', selecciona_usuario)

            lbl_id = Label(v2, text='ID')
            lbl_id.grid(row=5, column=1, padx=10, pady=5)
            ent_id = Listbox(v2, width=40, height=1)
            ent_id.grid(row=5, column=2, padx=10, pady=5)

            # ---------- Funciones ----------

            for cliente in obj_cliente.view():
                box_v2.insert(END, cliente[0] + ' - ' + cliente[1])
            ent_id.delete(0, END)

    def btn_v3_editar_f():
        grupo_id = ent_grupoid.get()
        nombre = drp_grupo.get()
        if grupo_id.replace(" ", "") == "" or nombre.replace(" ", "") == "":
            messagebox.showwarning('Editar Grupo', 'Seleccione un grupo para poder editarlo')
        else:
            clientes = []
            for cliente_id, _ in obj_grupo.members(nombre):
                clientes.append(cliente_id)

            v2 = Toplevel()
            v2.title('Editar Grupo')
            v2.iconbitmap('img/podemos.ico')
            v2.geometry('430x280')

            # ---------- Funciones ----------

            def selecciona_usuario(event):
                try:
                    global usuario
                    box_v2.curselection()
                    ind = box_v2.curselection()[0]
                    usuario = box_v2.get(ind)
                    id, nombre = usuario.split(' - ')
                    ent_id.delete(0, END)
                    ent_id.insert(END, id)
                except IndexError:
                    pass

            def btn_v2_añadir_f():
                id = ent_id.get(0)
                if id in clientes:
                    messagebox.showwarning('Editar grupo', 'El cliente ya esta en el grupo')
                else:
                    clientes.append(id)
                    obj_grupo.add(grupo_id, id)
                    messagebox.showinfo('Editar grupo', 'Se añadio al cliente {}, al grupo {}'.format(cliente_id, grupo_id))
                ent_id.delete(0, END)

            def btn_v2_eliminar_f():
                id = ent_id.get(0)
                if id.replace(" ", "") == "":
                    messagebox.showwarning('Editar grupo', 'Seleccione un cliente')
                elif id not in clientes:
                    messagebox.showwarning('Editar grupo', 'El cliente NO esta en el grupo')
                else:
                    if len(clientes) == 1:
                        messagebox.showerror('Editar grupo', 'El grupo no puede quedarse sin clientes')
                    else:
                        clientes.remove(id)
                        obj_grupo.remove(grupo_id, cliente_id)
                        messagebox.showinfo('Editar grupo', 'Se elimino al cliente {}, del grupo {}'.format(cliente_id, grupo_id))
                ent_id.delete(0, END)


            # ---------- Widgets ----------

            btn_v2_añadir = Button(v2, text='Añadir', width=15, command=btn_v2_añadir_f)
            btn_v2_añadir.grid(row=0, column=1, padx=10, pady=5)
            btn_v2_eliminar = Button(v2, text='Eliminar', width=15, command=btn_v2_eliminar_f)
            btn_v2_eliminar.grid(row=1, column=1, padx=10, pady=5)

            box_v2 = Listbox(v2, width=40, height=10)
            box_v2.grid(row=0, column=2, rowspan=4, padx=10, pady=5)
            box_v2.bind('<<ListboxSelect>>', selecciona_usuario)

            lbl_id = Label(v2, text='ID')
            lbl_id.grid(row=5, column=1, padx=10, pady=5)
            ent_id = Listbox(v2, width=40, height=1)
            ent_id.grid(row=5, column=2, padx=10, pady=5)

            # ---------- Funciones ----------

            for cliente in obj_cliente.view():
                box_v2.insert(END, cliente[0] + ' - ' + cliente[1])

            ent_id.delete(0, END)

    # ---------- Widgets ----------

    drp_grupo = StringVar()
    drp_grupo.set('Grupos')
    drp_v3_grupos = OptionMenu(v3, drp_grupo, *lst_grupos)
    drp_v3_grupos.grid(row=0, column=2, padx=20, pady=5)
    btn_v3_buscar = Button(v3, text='Buscar', width=15, command=btn_v3_buscar_f)
    btn_v3_buscar.grid(row=0, column=1, padx=10, pady=5)

    btn_v3_nuevo = Button(v3, text='Nuevo', width=15, command=btn_v3_nuevo_f)
    btn_v3_nuevo.grid(row=1, column=1, padx=10, pady=5)
    btn_v3_editar = Button(v3, text='Editar', width=15, command=btn_v3_editar_f)
    btn_v3_editar.grid(row=2, column=1, padx=10, pady=5)

    box_v3 = Listbox(v3, width=40, height=10)
    box_v3.grid(row=1, column=2, rowspan=4, padx=10, pady=5)

    lbl_id = Label(v3, text='ID')
    lbl_id.grid(row=5, column=1, padx=10, pady=5)
    ent_grupoid = Entry(v3, width=40)
    ent_grupoid.grid(row=5, column=2, padx=10, pady=5)

    lbl_nombre = Label(v3, text='Nombre')
    lbl_nombre.grid(row=6, column=1, padx=10, pady=5)
    ent_gruponombre = Entry(v3, width=40)
    ent_gruponombre.grid(row=6, column=2, padx=10, pady=5)


##################################################
# Ventana cuentas
##################################################
def cuentas_pop():
    v4 = Toplevel()
    v4.title('Cuentas')
    v4.iconbitmap('img/podemos.ico')
    v4.geometry('1100x250')

    # ---------- Funciones ----------

    def btn_v4_buscar_f():
        box_v4_cuentas.delete(0, END)
        for cuenta in obj_grupo.cuentas(drp_grupo.get()):
            box_v4_cuentas.insert(END, '{} - {} - ${} - ${}'.format(*cuenta))

    def btn_v4_buscar_detalles_f():
        try:
            box_v4_cuentas_detalles.delete(0, END)
            box_v4_cuentas_transacciones.delete(0, END)
            for registro in obj_grupo.calendario(ent_v4_id.get()):
                box_v4_cuentas_detalles.insert(END, '{} - {} - ${} - {}'.format(*registro))
            for registro in obj_grupo.transacciones(ent_v4_id.get()):
                box_v4_cuentas_transacciones.insert(END, '{} - {} - ${}'.format(*registro))
        except:
            messagebox.showwarning('Cuenta INFO', 'Ingrese un ID de una cuenta válido')

    def btn_v4_nueva_f():
        grupo = drp_grupo.get()
        grupo_id = obj_grupo.nombre_to_id(grupo)
        if grupo == 'Grupos':
            messagebox.showwarning('Nueva Cuenta', 'Seleccione un grupo para crear una cuenta')
        else:
            v4 = Toplevel()
            v4.title('Cuentas')
            v4.iconbitmap('img/podemos.ico')
            v4.geometry('270x150')

            # ---------- Funciones ----------

            def btn_v4_crear_f():
                try:
                    cuenta_id = int(ent_v4_cuentaid.get())
                    monto = int(ent_v4_monto.get())
                    num_pagos = int(ent_v4_num_pagos.get())
                    if monto <= 0 or num_pagos <= 0:
                        messagebox.showwarning('Cuenta nueva', 'Solo ingrese numeros positivos...')
                    else:
                        try:
                            obj_cuenta.new(cuenta_id, grupo_id, monto, num_pagos)
                            messagebox.showinfo('Cuenta creada', 'La cuenta {} fue creada exitosamente'.format(cuenta_id))
                            v4.destroy()
                        except mysql.connector.errors.IntegrityError:
                            messagebox.showerror('Nueva Cuenta', 'Se ingresaron datos incorrectos, intentelo nuevamente')
                except:
                    messagebox.showerror('Nueva Cuenta', 'Se ingresaron datos incorrectos, intentelo nuevamente')

            # ---------- Widgets ----------

            ent_v4_cuentaid = Entry(v4)
            ent_v4_cuentaid.grid(row=0, column=2, padx=10, pady=5)
            lbl_v4_cuentaid = Label(v4, text='cuenta ID')
            lbl_v4_cuentaid.grid(row=0, column=1, padx=10, pady=5)

            ent_v4_monto = Entry(v4)
            ent_v4_monto.grid(row=1, column=2, padx=10, pady=5)
            lbl_v4_monto = Label(v4, text='monto')
            lbl_v4_monto.grid(row=1, column=1, padx=10, pady=5)

            ent_v4_num_pagos = Entry(v4)
            ent_v4_num_pagos.grid(row=2, column=2, padx=10, pady=5)
            lbl_v4_num_pagos = Label(v4, text='Número de pagos')
            lbl_v4_num_pagos.grid(row=2, column=1, padx=10, pady=5)

            btn_v4_crear = Button(v4, text='Crear cuenta', command=btn_v4_crear_f)
            btn_v4_crear.grid(row=3, column=1, padx=10, pady=5, columnspan=2)

    # ---------- Widgets ----------

    drp_grupo = StringVar()
    drp_grupo.set('Grupos')
    drp_v4_grupos = OptionMenu(v4, drp_grupo, *lst_grupos)
    drp_v4_grupos.grid(row=0, column=1, padx=10, pady=5, columnspan=2)
    btn_v4_buscar_cuenta = Button(v4, text='Buscar cuentas', command=btn_v4_buscar_f)
    btn_v4_buscar_cuenta.grid(row=1, column=1, pady=5, columnspan=2)

    lbl_v4_cuentaid = Label(v4, text='cuenta ID')
    lbl_v4_cuentaid.grid(row=2, column=1)
    ent_v4_id = Entry(v4)
    ent_v4_id.grid(row=2, column=2)
    btn_v4_buscar_detalles = Button(v4, text='Detalles de la cuenta', command=btn_v4_buscar_detalles_f)
    btn_v4_buscar_detalles.grid(row=3, column=1, pady=5, columnspan=2)
    btn_v4_nueva = Button(v4, text='Nueva Cuenta', command=btn_v4_nueva_f)
    btn_v4_nueva.grid(row=4, column=1, pady=5, columnspan=2)

    lbl_v4_box_cuentas = Label(v4, text='Cuentas')
    lbl_v4_box_cuentas.grid(row=0, column=3)
    box_v4_cuentas = Listbox(v4, width=40, height=10)
    box_v4_cuentas.grid(row=1, column=3, rowspan=6, padx=10, pady=5)

    lbl_v4_box_calendario = Label(v4, text='Calendario')
    lbl_v4_box_calendario.grid(row=0, column=5)
    box_v4_cuentas_detalles = Listbox(v4, width=40, height=10)
    box_v4_cuentas_detalles.grid(row=1, column=5, rowspan=6, padx=10, pady=5)

    lbl_v4_box_transacciones = Label(v4, text='Transacciones')
    lbl_v4_box_transacciones.grid(row=0, column=7)
    box_v4_cuentas_transacciones = Listbox(v4, width=40, height=10)
    box_v4_cuentas_transacciones.grid(row=1, column=7, rowspan=6, padx=10, pady=5)


##################################################
# Ventana pagos
##################################################
def pagos_pop():
    v5 = Toplevel()
    v5.title('Pagos')
    v5.iconbitmap('img/podemos.ico')
    v5.geometry('220x120')

    # ---------- Funciones ----------
    def btn_v5_aplicar_f():
        try:
            cuenta_id = ent_v5_cuenta.get()
            pago = ent_v5_pago.get()
            num_pago, _ = obj_cuenta.pago_pendiente(cuenta_id)
            num, mensaje = obj_cuenta.pago(int(cuenta_id), int(pago))
            if num == 3:
                messagebox.showerror('Error', mensaje)
            if num == 2:
                messagebox.showwarning('Advertencia', mensaje)
            if num == 1:
                messagebox.showinfo('Info', mensaje)
                obj_cuenta.actualiza_cuenta(int(cuenta_id))
                v5.destroy()
        except:
            messagebox.showwarning('Advertencia', 'Inserte valores validos')

    # ---------- Widgets ----------

    lbl_v5_cuenta = Label(v5, text='Cuenta ID')
    lbl_v5_cuenta.grid(row=0, column=1, padx=10, pady=(15, 0))
    ent_v5_cuenta = Entry(v5)
    ent_v5_cuenta.grid(row=0, column=2, pady=5, columnspan=2)

    lbl_v5_pago = Label(v5, text='Pago')
    lbl_v5_pago.grid(row=2, column=1, padx=10, pady=5)
    ent_v5_pago = Entry(v5)
    ent_v5_pago.grid(row=2, column=2, padx=5, pady=(15, 0))

    btn_v5_aplicar = Button(v5, text='Aplicar', width=15, command=btn_v5_aplicar_f)
    btn_v5_aplicar.grid(row=4, column=1, padx=10, pady=(15, 0), columnspan=3)
