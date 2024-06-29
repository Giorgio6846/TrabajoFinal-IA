// Encuentra el botón por su ID
const startScreenshotBtn = document.getElementById("startScreenshot");

// Añade un event listener al botón
startScreenshotBtn.addEventListener("click", function handleClick() {
  // Configura un intervalo para hacer clic en el botón cada segundo
  setInterval(() => {
    startScreenshotBtn.click();
  }, 300);
  console.log("Boton presionado")
  // Deshabilita el botón después del primer clic para prevenir ejecuciones futuras
});
