const { ipcRenderer } = require('electron');


document.getElementById("startCapture").addEventListener("click", () => {
  ipcRenderer.send("solicitar-captura-pantalla");
});
