const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("electronAPI", {
  toggleScreenshot: (shouldTake) =>
    ipcRenderer.invoke("toggle-screenshot", shouldTake),
  getScreenshotStatus: () => ipcRenderer.invoke("get-screenshot-status"),
  onScreenshotTaken: (callback) => ipcRenderer.on("screenshot-taken", callback),
});
