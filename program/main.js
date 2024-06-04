require("electron-reload")(__dirname);
const { app, BrowserWindow, ipcMain, Menu } = require("electron");
const path = require("path");
const screenshot = require("screenshot-desktop");

const createWindow = () => {
  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, "preload.js"),
      contextIsolation: true, // Ensure context isolation is enabled
      nodeIntegration: false, // Disable node integration for security
      devTools: true,
      sandbox: false
    },
  })

  mainWindow.loadFile("./src/pages/index.html");
}

const mainMenu = [
    {
        label: 'Dev',
        submenu: [
            {
                role: 'toggledevtools'
            },
            {
                role: 'reload'
            },
            {
                role: 'forcereload'
            }
        ]
    },
    {
        label: 'Settings',
        submenu: [
            {
                label: 'Server Connection',
                click: async() => {
                    mainWindow.loadFile("./src/pages/serverConnection.html")
                    console.log("TEST")
                }
            }
        ]
    }
]

const menu = Menu.buildFromTemplate(mainMenu)
Menu.setApplicationMenu(menu)

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
