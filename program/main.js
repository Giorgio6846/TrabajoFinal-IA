const { app, BrowserWindow } = require('electron')

const createWindow  = () => {
    win = new BrowserWindow({
        width: 800,
        height: 600
    })

    win.loadFile('index.html')
}

app.on("ready", () => {
    createWindow()
});