const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronApi', {
	main: {
		isOSX: () => process.platform === 'darwin',
		isWindows: () => process.platform === 'win32',
		isLinux: () => /linux/.test(process.platform),
		openScreenSecurity: () => ipcRenderer.invoke('electronMain:openScreenSecurity'),
		getScreenAccess: () => ipcRenderer.invoke('electronMain:getScreenAccess'),
		getScreenSources: () => ipcRenderer.invoke('electronMain:screen:getSources'),
	}
});