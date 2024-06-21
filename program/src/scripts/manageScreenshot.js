setInterval(async () => {
  try {
    const imgPath = await window.electronAPI.takeScreenshot();
    document.getElementById("screenshot").src = `${imgPath}?${Date.now()}`;
  } catch (error) {
    console.error("Failed to take screenshot:", error);
  }
}, 1000);
