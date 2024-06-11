var zmq = require("zeromq");
sock = new zmq.Request();
const ipAddress = "tcp://127.0.0.1:5555";
const decoder = new TextDecoder();
const fs = require("fs");

const filePath = "../screenshots/screenshot-1.jpg";

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

    await sock.send(base64Image);
    console.log("Image sent to server");

    const result = await sock.receive();
    const dataServer = decoder.decode(result[0]);
    console.log("Received from server:", dataServer);
  }, 1000);
}

run(filePath);
