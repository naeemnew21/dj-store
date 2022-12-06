

let myVar;


function loaderFunction() {
  myVar = setTimeout(showPage, 3000);
}

function showPage() {
  document.getElementById("loader18").style.display = "none";
  document.getElementById("myDiv").style.display = "block";
}
