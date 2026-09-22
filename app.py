from flask import Flask, render_template, redirect, url_for, flash, request

from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user
)

from werkzeug.security import generate_password_hash, check_password_hash

from conexion.conexion import obtener_conexion

from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm

from models import Usuario


app = Flask(__name__)

# CLAVE SECRETA
app.config["SECRET_KEY"] = "kim-studio-clave-secreta-2026"


# CONFIGURACIÓN DE FLASK-LOGIN

login_manager = LoginManager(app)
login_manager.login_view = "login"


# CARGAR USUARIO DE LA SESIÓN

@login_manager.user_loader
def load_user(user_id):

    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, usuario
        FROM usuarios
        WHERE id = %s
    """, (user_id,))

    usuario = cursor.fetchone()

    cursor.close()
    conn.close()

    if usuario:
        return Usuario(usuario[0], usuario[1])

    return None


# INICIO

@app.route("/")
def inicio():

    return render_template("index.html")


# REGISTRO DE USUARIOS

@app.route("/registro", methods=["GET", "POST"])
def registro():

    if request.method == "POST":

        usuario = request.form.get("usuario")
        password = request.form.get("password")
        confirmar_password = request.form.get("confirmar_password")

        if not usuario or not password or not confirmar_password:

            flash("Todos los campos son obligatorios.", "danger")

            return render_template("registro.html")

        if password != confirmar_password:

            flash("Las contraseñas no coinciden.", "danger")

            return render_template("registro.html")

        conn = obtener_conexion()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id
            FROM usuarios
            WHERE usuario = %s
        """, (usuario,))

        usuario_existente = cursor.fetchone()

        if usuario_existente:

            cursor.close()
            conn.close()

            flash("El usuario ya existe.", "danger")

            return render_template("registro.html")

        password_hash = generate_password_hash(password)

        cursor.execute("""
            INSERT INTO usuarios (usuario, password)
            VALUES (%s, %s)
        """, (usuario, password_hash))

        conn.commit()

        cursor.close()
        conn.close()

        flash("Usuario registrado correctamente.", "success")

        return redirect(url_for("login"))

    return render_template("registro.html")


# LOGIN

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        usuario = request.form.get("usuario")
        password = request.form.get("password")

        conn = obtener_conexion()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, usuario, password
            FROM usuarios
            WHERE usuario = %s
        """, (usuario,))

        datos_usuario = cursor.fetchone()

        cursor.close()
        conn.close()

        if datos_usuario:

            password_correcta = check_password_hash(
                datos_usuario[2],
                password
            )

            if password_correcta:

                usuario_actual = Usuario(
                    datos_usuario[0],
                    datos_usuario[1]
                )

                login_user(usuario_actual)

                return redirect(url_for("dashboard"))

        flash("Usuario o contraseña incorrectos.", "danger")

    return render_template("login.html")


# DASHBOARD

@app.route("/dashboard")
@login_required
def dashboard():

    return render_template(
        "dashboard.html",
        usuario=current_user.usuario
    )


# CERRAR SESIÓN

@app.route("/logout")
@login_required
def logout():

    logout_user()

    flash("Sesión cerrada correctamente.", "success")

    return redirect(url_for("login"))


# ==========================================================
# PRODUCTOS
# ==========================================================

@app.route("/productos", methods=["GET", "POST"])
@login_required
def productos():

    form = ProductoForm()

    if form.validate_on_submit():

        conn = obtener_conexion()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO productos (nombre, precio, stock)
            VALUES (%s, %s, %s)
        """, (
            form.nombre.data,
            float(form.precio.data),
            form.cantidad.data
        ))

        conn.commit()

        cursor.close()
        conn.close()

        flash("Producto registrado correctamente.", "success")

        return redirect(url_for("productos"))

    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id_producto, nombre, precio, stock
        FROM productos
        ORDER BY id_producto
    """)

    productos = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "formulario_producto.html",
        form=form,
        productos=productos
    )


@app.route("/productos/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_producto(id):

    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id_producto, nombre, precio, stock
        FROM productos
        WHERE id_producto = %s
    """, (id,))

    producto = cursor.fetchone()

    if producto is None:

        cursor.close()
        conn.close()

        flash("Producto no encontrado.", "danger")

        return redirect(url_for("productos"))

    form = ProductoForm()

    if form.validate_on_submit():

        cursor.execute("""
            UPDATE productos
            SET nombre = %s,
                precio = %s,
                stock = %s
            WHERE id_producto = %s
        """, (
            form.nombre.data,
            float(form.precio.data),
            form.cantidad.data,
            id
        ))

        conn.commit()

        cursor.close()
        conn.close()

        flash("Producto actualizado correctamente.", "success")

        return redirect(url_for("productos"))

    if request.method == "GET":

        form.nombre.data = producto[1]
        form.precio.data = producto[2]
        form.cantidad.data = producto[3]

    cursor.close()
    conn.close()

    return render_template(
        "formulario_producto.html",
        form=form,
        productos=[]
    )


@app.route("/productos/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar_producto(id):

    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM productos
        WHERE id_producto = %s
    """, (id,))

    conn.commit()

    cursor.close()
    conn.close()

    flash("Producto eliminado correctamente.", "success")

    return redirect(url_for("productos"))


# ==========================================================
# CLIENTES
# ==========================================================

@app.route("/clientes", methods=["GET", "POST"])
@login_required
def clientes():

    form = ClienteForm()

    if form.validate_on_submit():

        conn = obtener_conexion()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO clientes (nombre, correo, telefono)
            VALUES (%s, %s, %s)
        """, (
            form.nombre.data,
            form.correo.data,
            form.telefono.data
        ))

        conn.commit()

        cursor.close()
        conn.close()

        flash("Cliente registrado correctamente.", "success")

        return redirect(url_for("clientes"))

    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id_cliente, nombre, correo, telefono
        FROM clientes
        ORDER BY id_cliente
    """)

    clientes = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "formulario_cliente.html",
        form=form,
        clientes=clientes
    )


@app.route("/clientes/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_cliente(id):

    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id_cliente, nombre, correo, telefono
        FROM clientes
        WHERE id_cliente = %s
    """, (id,))

    cliente = cursor.fetchone()

    if cliente is None:

        cursor.close()
        conn.close()

        flash("Cliente no encontrado.", "danger")

        return redirect(url_for("clientes"))

    form = ClienteForm()

    if form.validate_on_submit():

        cursor.execute("""
            UPDATE clientes
            SET nombre = %s,
                correo = %s,
                telefono = %s
            WHERE id_cliente = %s
        """, (
            form.nombre.data,
            form.correo.data,
            form.telefono.data,
            id
        ))

        conn.commit()

        cursor.close()
        conn.close()

        flash("Cliente actualizado correctamente.", "success")

        return redirect(url_for("clientes"))

    if request.method == "GET":

        form.nombre.data = cliente[1]
        form.correo.data = cliente[2]
        form.telefono.data = cliente[3]

    cursor.close()
    conn.close()

    return render_template(
        "formulario_cliente.html",
        form=form,
        clientes=[]
    )


@app.route("/clientes/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar_cliente(id):

    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM clientes
        WHERE id_cliente = %s
    """, (id,))

    conn.commit()

    cursor.close()
    conn.close()

    flash("Cliente eliminado correctamente.", "success")

    return redirect(url_for("clientes"))


# ==========================================================
# PROVEEDORES
# ==========================================================

@app.route("/proveedores", methods=["GET", "POST"])
@login_required
def proveedores():

    form = ProveedorForm()

    if form.validate_on_submit():

        conn = obtener_conexion()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO proveedores (nombre, empresa, correo)
            VALUES (%s, %s, %s)
        """, (
            form.nombre.data,
            form.empresa.data,
            form.correo.data
        ))

        conn.commit()

        cursor.close()
        conn.close()

        flash("Proveedor registrado correctamente.", "success")

        return redirect(url_for("proveedores"))

    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id_proveedor, nombre, empresa, correo
        FROM proveedores
        ORDER BY id_proveedor
    """)

    proveedores = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "formulario_proveedor.html",
        form=form,
        proveedores=proveedores
    )


@app.route("/proveedores/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_proveedor(id):

    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id_proveedor, nombre, empresa, correo
        FROM proveedores
        WHERE id_proveedor = %s
    """, (id,))

    proveedor = cursor.fetchone()

    if proveedor is None:

        cursor.close()
        conn.close()

        flash("Proveedor no encontrado.", "danger")

        return redirect(url_for("proveedores"))

    form = ProveedorForm()

    if form.validate_on_submit():

        cursor.execute("""
            UPDATE proveedores
            SET nombre = %s,
                empresa = %s,
                correo = %s
            WHERE id_proveedor = %s
        """, (
            form.nombre.data,
            form.empresa.data,
            form.correo.data,
            id
        ))

        conn.commit()

        cursor.close()
        conn.close()

        flash("Proveedor actualizado correctamente.", "success")

        return redirect(url_for("proveedores"))

    if request.method == "GET":

        form.nombre.data = proveedor[1]
        form.empresa.data = proveedor[2]
        form.correo.data = proveedor[3]

    cursor.close()
    conn.close()

    return render_template(
        "formulario_proveedor.html",
        form=form,
        proveedores=[]
    )


@app.route("/proveedores/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar_proveedor(id):

    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM proveedores
        WHERE id_proveedor = %s
    """, (id,))

    conn.commit()

    cursor.close()
    conn.close()

    flash("Proveedor eliminado correctamente.", "success")

    return redirect(url_for("proveedores"))


# ==========================================================
# FACTURACIÓN
# ==========================================================

@app.route("/facturacion", methods=["GET", "POST"])
@login_required
def facturacion():

    form = FacturacionForm()

    # CREAR FACTURA

    if form.validate_on_submit():

        conn = obtener_conexion()
        cursor = conn.cursor()

        # BUSCAR CLIENTE POR NOMBRE
        cursor.execute("""
            SELECT id_cliente
            FROM clientes
            WHERE nombre = %s
        """, (form.cliente.data,))

        cliente = cursor.fetchone()

        # BUSCAR PRODUCTO POR NOMBRE
        cursor.execute("""
            SELECT id_producto
            FROM productos
            WHERE nombre = %s
        """, (form.producto.data,))

        producto = cursor.fetchone()

        if cliente is None:

            cursor.close()
            conn.close()

            flash("El cliente no existe. Regístrelo primero.", "danger")

            return render_template(
                "formulario_facturacion.html",
                form=form,
                facturas=[]
            )

        if producto is None:

            cursor.close()
            conn.close()

            flash("El producto no existe. Regístrelo primero.", "danger")

            return render_template(
                "formulario_facturacion.html",
                form=form,
                facturas=[]
            )

        # CALCULAR TOTAL

        total = float(form.cantidad.data) * float(form.precio.data)

        # CREAR FACTURA

        cursor.execute("""
            INSERT INTO facturas (id_cliente, total)
            VALUES (%s, %s)
            RETURNING id_factura
        """, (
            cliente[0],
            total
        ))

        factura = cursor.fetchone()
        id_factura = factura[0]

        # CREAR DETALLE

        cursor.execute("""
            INSERT INTO detalle_factura
            (id_factura, id_producto, cantidad, precio)
            VALUES (%s, %s, %s, %s)
        """, (
            id_factura,
            producto[0],
            form.cantidad.data,
            float(form.precio.data)
        ))

        conn.commit()

        cursor.close()
        conn.close()

        flash("Factura registrada correctamente.", "success")

        return redirect(url_for("facturacion"))

    # ======================================================
    # JOIN PARA MOSTRAR INFORMACIÓN RELACIONADA
    # ======================================================

    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            f.id_factura,
            c.nombre AS cliente,
            p.nombre AS producto,
            df.cantidad,
            df.precio,
            f.total,
            f.fecha
        FROM facturas f
        INNER JOIN clientes c
            ON f.id_cliente = c.id_cliente
        INNER JOIN detalle_factura df
            ON f.id_factura = df.id_factura
        INNER JOIN productos p
            ON df.id_producto = p.id_producto
        ORDER BY f.id_factura
    """)

    facturas = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "formulario_facturacion.html",
        form=form,
        facturas=facturas
    )


# EJECUTAR APLICACIÓN

if __name__ == "__main__":
    app.run(debug=True)