from flask import Flask, render_template, redirect, url_for, flash

from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm


app = Flask(__name__)

# Clave secreta para Flask-WTF y protección CSRF
app.config["SECRET_KEY"] = "kim-studio-clave-secreta-2026"


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/productos", methods=["GET", "POST"])
def productos():

    form = ProductoForm()

    if form.validate_on_submit():

        flash("Producto registrado correctamente.", "success")

        return redirect(url_for("productos"))

    return render_template(
        "formulario_producto.html",
        form=form
    )


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


if __name__ == "__main__":
    app.run(debug=True)