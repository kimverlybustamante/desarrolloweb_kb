// PROYECTO INTEGRADOR - SEMANA 8
// Plataforma Musical Kim Studio

// FORMULARIO

const formulario = document.getElementById("formularioProyecto");
const lista = document.getElementById("listaProyectos");
const contador = document.getElementById("contador");

// CAMPOS

const nombre = document.getElementById("nombreProyecto");
const artista = document.getElementById("artista");
const categoria = document.getElementById("categoria");
const descripcion = document.getElementById("descripcion");

// MENSAJES

const errorNombre = document.getElementById("errorNombre");
const errorArtista = document.getElementById("errorArtista");
const errorCategoria = document.getElementById("errorCategoria");
const errorDescripcion = document.getElementById("errorDescripcion");
const mensajeGeneral = document.getElementById("mensajeGeneral");

// SPINNER

const spinner = document.getElementById("spinnerCarga");

// ARREGLO

let proyectos = [];

// MOSTRAR PROYECTOS

function mostrarProyectos() {

    lista.innerHTML = "";

    if (proyectos.length === 0) {

        lista.innerHTML = `

        <div class="alert alert-warning text-center">

            No existen proyectos registrados.

        </div>

        `;

        contador.textContent = 0;

        return;

    }

    contador.textContent = proyectos.length;

    proyectos.forEach(function (proyecto, index) {

        lista.innerHTML += `

        <div class="card shadow mb-4">

            <div class="card-body">

                <h4 class="card-title">

                    ${proyecto.nombre}

                </h4>

                <span class="badge bg-primary">

                    ${proyecto.categoria}

                </span>

                <hr>

                <p>

                    <strong>Artista:</strong>

                    ${proyecto.artista}

                </p>

                <p>

                    <strong>Descripción:</strong>

                    ${proyecto.descripcion}

                </p>

                <button
                    class="btn btn-info me-2"
                    onclick="verProyecto(${index})">

                    Ver detalles

                </button>

                <button
                    class="btn btn-danger"
                    onclick="eliminarProyecto(${index})">

                    Eliminar

                </button>

            </div>

        </div>

        `;

    });

}

// ELIMINAR PROYECTO

function eliminarProyecto(indice) {

    proyectos.splice(indice, 1);

    mostrarProyectos();

    mensajeGeneral.innerHTML = `

    <div class="alert alert-warning alert-dismissible fade show">

        Proyecto eliminado correctamente.

        <button
            type="button"
            class="btn-close"
            data-bs-dismiss="alert">
        </button>

    </div>

    `;

}

// VER DETALLES (MODAL)


function verProyecto(indice) {

    const proyecto = proyectos[indice];

    document.querySelector("#modalServicios .modal-title").textContent =
        proyecto.nombre;

    document.querySelector("#modalServicios .modal-body").innerHTML = `

        <p><strong>Nombre:</strong> ${proyecto.nombre}</p>

        <p><strong>Artista:</strong> ${proyecto.artista}</p>

        <p><strong>Categoría:</strong> ${proyecto.categoria}</p>

        <p><strong>Descripción:</strong><br>${proyecto.descripcion}</p>

    `;

    const modal = new bootstrap.Modal(document.getElementById("modalServicios"));

    modal.show();

}

// VALIDACIONES

function validarNombre() {

    if (nombre.value.trim().length < 3) {

        nombre.classList.add("is-invalid");
        nombre.classList.remove("is-valid");

        errorNombre.innerHTML =
            "<small class='text-danger'>El nombre debe tener mínimo 3 caracteres.</small>";

        return false;

    }

    nombre.classList.remove("is-invalid");
    nombre.classList.add("is-valid");

    errorNombre.innerHTML =
        "<small class='text-success'>Nombre válido.</small>";

    return true;

}

function validarArtista() {

    if (artista.value.trim() === "") {

        artista.classList.add("is-invalid");
        artista.classList.remove("is-valid");

        errorArtista.innerHTML =
            "<small class='text-danger'>Ingrese el nombre del artista.</small>";

        return false;

    }

    artista.classList.remove("is-invalid");
    artista.classList.add("is-valid");

    errorArtista.innerHTML =
        "<small class='text-success'>Artista válido.</small>";

    return true;

}

function validarCategoria() {

    if (categoria.value === "") {

        categoria.classList.add("is-invalid");
        categoria.classList.remove("is-valid");

        errorCategoria.innerHTML =
            "<small class='text-danger'>Seleccione una categoría.</small>";

        return false;

    }

    categoria.classList.remove("is-invalid");
    categoria.classList.add("is-valid");

    errorCategoria.innerHTML =
        "<small class='text-success'>Categoría válida.</small>";

    return true;

}

function validarDescripcion() {

    if (descripcion.value.trim().length < 10) {

        descripcion.classList.add("is-invalid");
        descripcion.classList.remove("is-valid");

        errorDescripcion.innerHTML =
            "<small class='text-danger'>La descripción debe tener mínimo 10 caracteres.</small>";

        return false;

    }

    descripcion.classList.remove("is-invalid");
    descripcion.classList.add("is-valid");

    errorDescripcion.innerHTML =
        "<small class='text-success'>Descripción válida.</small>";

    return true;

}

// VALIDACIÓN EN TIEMPO REAL

nombre.addEventListener("input", validarNombre);
nombre.addEventListener("blur", validarNombre);

artista.addEventListener("input", validarArtista);
artista.addEventListener("blur", validarArtista);

categoria.addEventListener("change", validarCategoria);

descripcion.addEventListener("input", validarDescripcion);
descripcion.addEventListener("blur", validarDescripcion);

// REGISTRAR PROYECTO

formulario.addEventListener("submit", function (event) {

    event.preventDefault();

    let nombreValido = validarNombre();
    let artistaValido = validarArtista();
    let categoriaValida = validarCategoria();
    let descripcionValida = validarDescripcion();

    if (!nombreValido || !artistaValido || !categoriaValida || !descripcionValida) {

        mensajeGeneral.innerHTML = `

        <div class="alert alert-danger alert-dismissible fade show">

            Debe corregir los errores antes de registrar el proyecto.

            <button
                type="button"
                class="btn-close"
                data-bs-dismiss="alert">
            </button>

        </div>

        `;

        return;

    }

    // Mostrar Spinner

    spinner.style.display = "block";

    setTimeout(function () {

        spinner.style.display = "none";

        proyectos.push({

            nombre: nombre.value.trim(),
            artista: artista.value.trim(),
            categoria: categoria.value,
            descripcion: descripcion.value.trim()

        });

        mostrarProyectos();

        mensajeGeneral.innerHTML = `

        <div class="alert alert-success alert-dismissible fade show">

            <strong>¡Éxito!</strong>

            El proyecto fue registrado correctamente.

            <button
                type="button"
                class="btn-close"
                data-bs-dismiss="alert">
            </button>

        </div>

        `;

        formulario.reset();

        nombre.classList.remove("is-valid");
        artista.classList.remove("is-valid");
        categoria.classList.remove("is-valid");
        descripcion.classList.remove("is-valid");

        errorNombre.innerHTML = "";
        errorArtista.innerHTML = "";
        errorCategoria.innerHTML = "";
        errorDescripcion.innerHTML = "";

    }, 1500);

});

// INICIO DEL SISTEMA

mostrarProyectos();