const {app, BrowserWindow, ipcMain, systemPreferences, desktopCapturer, Menu} = require('electron');
const path = require('path');
const IS_OSX = process.platform === 'darwin';

try {
    require('electron-reloader')(module);
} catch {}

console.log(systemPreferences.getMediaAccessStatus('screen'))

const createWindow  = () => {
    win = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            devTools: true,
            sandbox: false
        }
    })

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
    }
]

const menu = Menu.buildFromTemplate(mainMenu)
Menu.setApplicationMenu(menu)
app.on("ready", () => {
    createWindow()
});