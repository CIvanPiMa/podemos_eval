from front2 import *

##################################################
# Ventana Principal(V1)
##################################################
actualiza_calendario()
v1 = Tk()
v1.title('Podemos - GUI de juguete')
v1.iconbitmap('img/podemos.ico')
v1.geometry('300x170')

# ---------- Widgets ----------

btn_v1_clientes = Button(v1, text='Clientes', command=clientes_pop, width=20)
btn_v1_clientes.grid(row=0, column=1, padx=10, pady=5)
btn_v1_grupos = Button(v1, text='Grupos', command=grupos_pop, width=20)
btn_v1_grupos.grid(row=1, column=1, padx=10, pady=5)
btn_v1_cuentas = Button(v1, text='Cuentas', command=cuentas_pop, width=20)
btn_v1_cuentas.grid(row=2, column=1, padx=10, pady=5)
btn_v1_pagos = Button(v1, text='Pagos', command=pagos_pop, width=20)
btn_v1_pagos.grid(row=3, column=1, padx=10, pady=5)

lbl_v1_clientes = Label(v1, text='Ver clientes')
lbl_v1_clientes.grid(row=0, column=2, pady=(15, 0))
lbl_v1_grupos = Label(v1, text='Ver grupos')
lbl_v1_grupos.grid(row=1, column=2, pady=5)
lbl_v1_cuentas = Label(v1, text='Ver cuentas')
lbl_v1_cuentas.grid(row=2, column=2, pady=5)
lbl_v1_pagos = Label(v1, text='Realizar pagos')
lbl_v1_pagos.grid(row=3, column=2, pady=20)

v1.mainloop()
