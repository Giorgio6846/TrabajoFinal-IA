let mouseIsDown = false;

addEventListener("mousedown", (event) => {
  mouseIsDown = true;
});

addEventListener("mousemove", (event) => {
  if (mouseIsDown) {
    console.log(`Mouse position: ${event.clientX}, ${event.clientY}`);
    mouseIsDown = false;
  }
});
