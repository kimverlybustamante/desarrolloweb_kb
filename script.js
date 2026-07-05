const formulario = document.getElementById("formularioProyecto");
const lista = document.getElementById("listaProyectos");
const contador = document.getElementById("contador");

let total = 0;

const nombre = document.getElementById("nombreProyecto");
const artista = document.getElementById("artista");
const categoria = document.getElementById("categoria");
const descripcion = document.getElementById("descripcion");

const errorNombre = document.getElementById("errorNombre");
const errorArtista = document.getElementById("errorArtista");
const errorCategoria = document.getElementById("errorCategoria");
const errorDescripcion = document.getElementById("errorDescripcion");
const mensajeGeneral = document.getElementById("mensajeGeneral");

// VALIDAR NOMBRE
function validarNombre(){

if(nombre.value.trim().length < 3){

nombre.classList.add("is-invalid");
nombre.classList.remove("is-valid");

errorNombre.innerHTML="<small class='text-danger'>El nombre debe tener mínimo 3 caracteres.</small>";

return false;

}else{

nombre.classList.remove("is-invalid");
nombre.classList.add("is-valid");

errorNombre.innerHTML="<small class='text-success'>Nombre válido.</small>";

return true;

}

}

// VALIDAR ARTISTA
function validarArtista(){

if(artista.value.trim()===""){

artista.classList.add("is-invalid");
artista.classList.remove("is-valid");

errorArtista.innerHTML="<small class='text-danger'>Ingrese el nombre del artista.</small>";

return false;

}else{

artista.classList.remove("is-invalid");
artista.classList.add("is-valid");

errorArtista.innerHTML="<small class='text-success'>Artista válido.</small>";

return true;

}

}

// VALIDAR CATEGORÍA
function validarCategoria(){

if(categoria.value===""){

categoria.classList.add("is-invalid");
categoria.classList.remove("is-valid");

errorCategoria.innerHTML="<small class='text-danger'>Seleccione una categoría.</small>";

return false;

}else{

categoria.classList.remove("is-invalid");
categoria.classList.add("is-valid");

errorCategoria.innerHTML="<small class='text-success'>Categoría válida.</small>";

return true;

}

}

// VALIDAR DESCRIPCIÓN
function validarDescripcion(){

if(descripcion.value.trim().length < 10){

descripcion.classList.add("is-invalid");
descripcion.classList.remove("is-valid");

errorDescripcion.innerHTML="<small class='text-danger'>La descripción debe tener mínimo 10 caracteres.</small>";

return false;

}else{

descripcion.classList.remove("is-invalid");
descripcion.classList.add("is-valid");

errorDescripcion.innerHTML="<small class='text-success'>Descripción válida.</small>";

return true;

}

}

// EVENTOS EN TIEMPO REAL

nombre.addEventListener("input", validarNombre);
nombre.addEventListener("blur", validarNombre);

artista.addEventListener("input", validarArtista);
artista.addEventListener("blur", validarArtista);

categoria.addEventListener("change", validarCategoria);

descripcion.addEventListener("input", validarDescripcion);
descripcion.addEventListener("blur", validarDescripcion);

// REGISTRAR

formulario.addEventListener("submit", function(event){

event.preventDefault();

let nombreValido = validarNombre();
let artistaValido = validarArtista();
let categoriaValida = validarCategoria();
let descripcionValida = validarDescripcion();

if(!nombreValido || !artistaValido || !categoriaValida || !descripcionValida){

mensajeGeneral.innerHTML="<div class='alert alert-danger'>Debe corregir los errores antes de registrar.</div>";

return;

}

mensajeGeneral.innerHTML="<div class='alert alert-success'>Proyecto registrado correctamente.</div>";

let proyecto = document.createElement("div");

proyecto.className="card p-3 mt-3";

proyecto.innerHTML=`

<h3>${nombre.value}</h3>

<p><strong>Artista:</strong> ${artista.value}</p>

<p><strong>Categoría:</strong> ${categoria.value}</p>

<p><strong>Descripción:</strong> ${descripcion.value}</p>

<button class="btn btn-danger mt-2">
Eliminar
</button>

`;

lista.appendChild(proyecto);

total++;

contador.textContent = total;

let botonEliminar = proyecto.querySelector("button");

botonEliminar.addEventListener("click", function(){

proyecto.remove();

total--;

contador.textContent = total;

});

formulario.reset();

nombre.classList.remove("is-valid");
artista.classList.remove("is-valid");
categoria.classList.remove("is-valid");
descripcion.classList.remove("is-valid");

errorNombre.innerHTML="";
errorArtista.innerHTML="";
errorCategoria.innerHTML="";
errorDescripcion.innerHTML="";

});