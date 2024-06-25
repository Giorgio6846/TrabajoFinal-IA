const { app, BrowserWindow, ipcMain, Menu } = require("electron");
const path = require("path");
const screenshot = require("screenshot-desktop");
const fs = require("fs");

let mainWindow;
let screenshotInterval;

// Parámetros iniciales
let appSettings = {
  tomarScreenshot: false
};

// Función para guardar los ajustes
function saveSettings() {
  fs.writeFileSync(path.join(__dirname, 'settings.json'), JSON.stringify(appSettings));
}

// Función para cargar los ajustes
function loadSettings() {
  try {
    const data = fs.readFileSync(path.join(__dirname, 'settings.json'));
    appSettings = JSON.parse(data);
  } catch (error) {
    console.log('No se encontraron ajustes previos, usando los predeterminados');
    saveSettings();
  }
}

const createWindow = () => {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 720,
    webPreferences: {
      preload: path.join(__dirname, "preload.js"),
      contextIsolation: true,
      nodeIntegration: false,
      devTools: true,
      sandbox: false,
    },
  });

  mainWindow.loadFile("./src/pages/index.html");
};

app.whenReady().then(() => {
  loadSettings();
  createWindow();
  
  if (appSettings.tomarScreenshot) {
    startScreenshotCapture();
  }

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

function startScreenshotCapture() {
  if (screenshotInterval) {
    clearInterval(screenshotInterval);
  }
  
  screenshotInterval = setInterval(async () => {
    try {
      const imgPath = path.join(__dirname, "/screenshots", `screenshot-1.jpg`);
      await screenshot({ filename: imgPath });
      mainWindow.webContents.send('screenshot-taken', imgPath);
    } catch (error) {
      console.error("Failed to take screenshot:", error);
    }
  }, 1000);
}

function stopScreenshotCapture() {
  if (screenshotInterval) {
    clearInterval(screenshotInterval);
    screenshotInterval = null;
  }
}

ipcMain.handle("toggle-screenshot", async (event, shouldTake) => {
  appSettings.tomarScreenshot = shouldTake;
  saveSettings();
  
  if (shouldTake) {
    startScreenshotCapture();
  } else {
    stopScreenshotCapture();
  }
  
  return appSettings.tomarScreenshot;
});

ipcMain.handle("get-screenshot-status", async () => {
  return appSettings.tomarScreenshot;
});

var zmq = require("zeromq");
sock = new zmq.Request();
const ipAddress = "tcp://127.0.0.1:5555";
const decoder = new TextDecoder();

const filePath = "./screenshots/screenshot-1.jpg";

function imageToBase64(filePath) {
  const image = fs.readFileSync(filePath);
  const base64Image = image.toString("base64");
  return base64Image;
}

async function run(filePath) {
  sock.connect(ipAddress);
  console.log("Connected to server at " + ipAddress);

  setInterval(async () => {
    const base64Image = imageToBase64(filePath);
    //base64Image = JSON.stringify(base64Image);
    requestJSONData = {
      "image": base64Image,
    };
    dataToServer = JSON.stringify(requestJSONData);
    await sock.send(dataToServer);
    console.log("Image sent to server");

    const result = await sock.receive();
    const dataServer = decoder.decode(result[0]);
    console.log("Received from server:", dataServer);
  }, 1000);
}

run(filePath)