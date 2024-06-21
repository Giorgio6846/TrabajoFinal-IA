let isCapturing = false;

async function updateScreenshotStatus() {
  const status = await window.electronAPI.getScreenshotStatus();
  document.getElementById('screenshotStatus').textContent = status ? 'Capturing' : 'Not capturing';
  document.getElementById('toggleScreenshotBtn').textContent = status ? 'Stop Capture' : 'Start Capture';
  isCapturing = status;
}

document.getElementById('toggleScreenshotBtn').addEventListener('click', async () => {
  const newStatus = await window.electronAPI.toggleScreenshot(!isCapturing);
  await updateScreenshotStatus();
});

window.electronAPI.onScreenshotTaken((event, imgPath) => {
  document.getElementById('screenshot').src = `file://${imgPath}`;
  document.getElementById('screenshot').style.display = 'block';
});

// Actualizar el estado inicial
updateScreenshotStatus();