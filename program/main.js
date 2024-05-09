const {app, BrowserWindow, ipcMain, systemPreferences, desktopCapturer} = require('electron');
const { openSystemPreferences } = require("electron-util");
const IS_OSX = process.platform === 'darwin';

const createWindow  = () => {
    win = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            devTools: true,
            sandbox: false
        }
    })

    win.loadFile('index.html')
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
    }
]

app.on("ready", () => {
    createWindow()
});