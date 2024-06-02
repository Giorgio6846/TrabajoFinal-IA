const { app, BrowserWindow } = require('electron');

<<<<<<< Updated upstream:program/index.js
try {
    require('electron-reloader')(module);
} catch {}

console.log(systemPreferences.getMediaAccessStatus('screen'))
=======
const url = require("url");
const path = require("path");
>>>>>>> Stashed changes:program/main.js

let mainWindow

<<<<<<< Updated upstream:program/index.js
    win.loadFile(path.join(__dirname,'src','views','mainPage.html'))
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
                label: 'Screen Capture',
                click: async() => {
                    win.loadFile(path.join(__dirname,'src','views','screenCapture.html'))                
                }
            },
            {
                label: 'Server Connection',
                click: async() => {
                    win.loadFile(path.join(__dirname,'src','views','serverConnection.html'))
                }
            }
        ]
=======
function createWindow() {
  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true
>>>>>>> Stashed changes:program/main.js
    }
  })

  mainWindow.loadURL(
    url.format({
      pathname: path.join(__dirname, `./dist/index.html`),
      protocol: "file:",
      slashes: true
    })
  );
  mainWindow.on('closed', function () {
    mainWindow = null
  })
}
console.log(app);
app.on('ready', createWindow)

app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') app.quit()
})

app.on('activate', function () {
  if (mainWindow === null) createWindow()
})