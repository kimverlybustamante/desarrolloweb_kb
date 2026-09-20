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

# Clave secreta para Flask-WTF y las sesiones
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

        # Encriptar la contraseña antes de guardarla
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


# PRODUCTOS

@app.route("/productos", methods=["GET", "POST"])
@login_required
def productos():

    form = ProductoForm()

    # AGREGAR PRODUCTO
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

    # LISTAR PRODUCTOS
    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id_producto, nombre, precio, stock
        FROM productos
    """)

    productos = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "formulario_producto.html",
        form=form,
        productos=productos
    )


# MODIFICAR PRODUCTO

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

    # ACTUALIZAR PRODUCTO
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

    # CARGAR DATOS ACTUALES
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


# ELIMINAR PRODUCTO

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


# CLIENTES

@app.route("/clientes", methods=["GET", "POST"])
@login_required
def clientes():

    form = ClienteForm()

    if form.validate_on_submit():

        flash("Cliente registrado correctamente.", "success")

        return redirect(url_for("clientes"))

    return render_template(
        "formulario_cliente.html",
        form=form
    )


# PROVEEDORES

@app.route("/proveedores", methods=["GET", "POST"])
@login_required
def proveedores():

    form = ProveedorForm()

    if form.validate_on_submit():

        flash("Proveedor registrado correctamente.", "success")

        return redirect(url_for("proveedores"))

    return render_template(
        "formulario_proveedor.html",
        form=form
    )


# FACTURACIÓN

@app.route("/facturacion", methods=["GET", "POST"])
@login_required
def facturacion():

    form = FacturacionForm()

    if form.validate_on_submit():

        flash("Factura procesada correctamente.", "success")

        return redirect(url_for("facturacion"))

    return render_template(
        "formulario_facturacion.html",
        form=form
    )


# EJECUTAR APLICACIÓN

if __name__ == "__main__":
    app.run(debug=True)