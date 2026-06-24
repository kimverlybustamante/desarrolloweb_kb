const formulario = document.getElementById("formularioProyecto");

const lista = document.getElementById("listaProyectos");

const contador = document.getElementById("contador");


let total = 0;



formulario.addEventListener("submit", function(event){


event.preventDefault();



let nombre = document.getElementById("nombreProyecto").value;

let artista = document.getElementById("artista").value;

let categoria = document.getElementById("categoria").value;



if(nombre === "" || artista === "" || categoria === ""){


alert("Complete todos los campos");


return;

}



let proyecto = document.createElement("div");


proyecto.className = "card p-3 mt-3";



proyecto.innerHTML = `

<h3>${nombre}</h3>

<p>Artista: ${artista}</p>

<p>Categoría: ${categoria}</p>


<button class="btn btn-danger">

Eliminar

</button>

`;



lista.appendChild(proyecto);



total++;


contador.textContent = total;




let boton = proyecto.querySelector("button");



boton.addEventListener("click", function(){


proyecto.remove();


total--;


contador.textContent = total;


});



formulario.reset();


});