from flask import Flask, render_template, redirect, url_for, flash, request

from conexion.conexion import obtener_conexion

from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm


app = Flask(__name__)

# Clave secreta para Flask-WTF y protección CSRF
app.config["SECRET_KEY"] = "kim-studio-clave-secreta-2026"



# INICIO

@app.route("/")
def inicio():
    return render_template("index.html")



# PRODUCTOS
# LISTAR + AGREGAR

@app.route("/productos", methods=["GET", "POST"])
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
def editar_producto(id):

    conn = obtener_conexion()
    cursor = conn.cursor()

    # Buscar producto
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

    # ACTUALIZAR
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

    # Cargar datos actuales en el formulario
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