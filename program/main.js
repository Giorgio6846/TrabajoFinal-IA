require("electron-reload")(__dirname);
const { app, BrowserWindow, ipcMain } = require("electron");
const path = require("path");
const screenshot = require("screenshot-desktop");

function createWindow() {
  const mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, "preload.js"),
      contextIsolation: true, // Ensure context isolation is enabled
      nodeIntegration: false, // Disable node integration for security
    },
  });

  mainWindow.loadFile("./src/pages/index.html");
}

app.whenReady().then(() => {
  createWindow();

  app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
  }
});

ipcMain.handle("take-screenshot", async () => {
  try {
    const timestamp = Date.now();
    const imgPath = path.join(
      __dirname,
      "/screenshots",
      `screenshot-${timestamp}.jpg`
    );
    await screenshot({ filename: imgPath });
    return imgPath;
  } catch (error) {
    console.error("Failed to take screenshot:", error);
    throw error;
  }
});
