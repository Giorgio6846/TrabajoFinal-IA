const { defineConfig } = require("@vue/cli-service");
module.exports = {
  pluginOptions: {
    electron: {
      mainProcessFile: "src/background.js",
      rendererProcessFile: "src/main.js",
    },
  },
};
