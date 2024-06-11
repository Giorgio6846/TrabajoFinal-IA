require("electron-reload")(__dirname);
const { app, BrowserWindow, ipcMain, Menu } = require("electron");
const path = require("path");
const screenshot = require("screenshot-desktop");

contador = 0;

const createWindow = () => {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 720,
    webPreferences: {
      preload: path.join(__dirname, "preload.js"),
      contextIsolation: true, // Ensure context isolation is enabled
      nodeIntegration: false, // Disable node integration for security
      devTools: true,
      sandbox: false,
    },
  });

  mainWindow.loadFile("./src/pages/index.html");
};

const mainMenu = [
  {
    label: "Dev",
    submenu: [
      {
        role: "toggledevtools",
      },
      {
        role: "reload",
      },
      {
        role: "forcereload",
      },
    ],
  },
  {
    label: "Settings",
    submenu: [
      {
        label: "Server Connection",
        click: async () => {
          mainWindow.loadFile("./src/pages/serverConnection.html");
          console.log("TEST");
        },
      },
    ],
  },
];

const menu = Menu.buildFromTemplate(mainMenu);
Menu.setApplicationMenu(menu);

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
    contador = contador + 1;
    const timestamp = Date.now();
    const imgPath = path.join(
      __dirname,
      "/screenshots",
      `screenshot-${contador}.jpg`
    );
    await screenshot({ filename: imgPath });
    return imgPath;
  } catch (error) {
    console.error("Failed to take screenshot:", error);
    throw error;
  }
});

var zmq = require("zeromq");
sock = new zmq.Request();
const ipAddress = "tcp://127.0.0.1:5555";
const decoder = new TextDecoder();
const fs = require("fs");

const filePath = "./screenshots/screenshot-1.jpg";

function imageToBase64(filePath) {
  const image = fs.readFileSync(filePath);
  const base64Image = image.toString("base64");
  return base64Image;
}

async function run(filePath) {
  sock.connect(ipAddress);
  console.log("Connected to server at tcp://127.0.0.1:5555");

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

run(filePath);
