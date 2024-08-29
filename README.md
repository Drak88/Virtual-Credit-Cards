# Virtual Credit Cards

(README) Version in Spanish.

Un simulador de tarjetas de debito virtuales, y si, a pesar de que el nombre del proyecto dice lo contrario, son de debito. Y ante todos son tarjetas falsas, que sirven para mera experimentacion.

\[Esto es un proyecto sin fines de lucro. Aplicando la **Licencia CC BY** (Creative Commons Attribution).\]

# Requisitos

- Python. Descargalo desde https://www.python.org/downloads/

# Montar el programa / Setup

(Despues de haber instalado Python) Abre "vcc_server.pyw" y "vi_cr_ca.pyw" con Python:

```
py vcc_server.pyw
```
```
py vi_cr_ca.pyw
```

Se puede abrir con dos terminales o abrirlos directamente establenciendo Python como ejecutable predeterminado a los archivos `.pyw`.

# Como usarlo / guia de uso

El programa `vcc_server.pyw` es el servidor, en este programa se guardan y muestran todas las cuentas y sus datos. Este puede:
- **Crear** cuentas; dando una identificacion (*"Cedula"*), una contraseña y un saldo inicial. Estas cuentas contienen saldo / dinero el cual sirve para hacer transacciones en el otro programa; `vi_cr_ca.pyw`.
- **Modificar** el saldo de las cuentas.
- **Borrar** cuentas.
- Dar una **bonificacion** *economica* (**"Bono"**) a una cuenta.

El programa `vi_cr_ca.pyw` por su parte es el cliente, o mejor dicha el programa donde se realizan las transacciones. Al abrir el programa deberas establecer una cuenta beneficiaria (la cual queda registrada (con un tipo de encriptacion que no sirve para encriptar pero no creo que lo necesites encriptar demasiado seguro pues esto no sirve para nada en la vida cotidiana), la cuenta beneficiara debera ser establecida (**no registrada de nuevo**) al abrir el programa, para abrir el menu donde se registran y establecen los beneficiarios (**"Destinatarios"**) debes presionar `0` en la primera etapa de la transaccion, donde se ingresa el monto.
