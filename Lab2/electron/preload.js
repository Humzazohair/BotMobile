// All of the Node.js APIs are available in the preload process.
// It has the same sandbox as a Chrome extension.
window.addEventListener('DOMContentLoaded', () => {
  const replaceText = (selector, text) => {
    const element = document.getElementById(selector)
    if (element) element.innerText = text
  }

  for (const type of ['chrome', 'node', 'electron']) {
    replaceText(`${type}-version`, process.versions[type])
  }
})

FORWARD = "FORWARD!"
LEFT = "LEFT!"
RIGHT = "RIGHT!"
BACK = "BACK!"


document.addEventListener('DOMContentLoaded', function() {
  // Your code here will run once the DOM is fully loaded
  const upArrow = document.getElementById('upArrow');
  const leftArrow = document.getElementById('leftArrow');
  const rightArrow = document.getElementById('rightArrow');
  const downArrow = document.getElementById('downArrow');
  if (!upArrow || !leftArrow || !rightArrow || !downArrow) {
    console.log("ARROW(S) NOT FOUND");
    return;
  }
  movingForward = false;
  movingLeft = false;
  movingRight = false;
  movingBack = false;

  function addEventListeners(direction, message, moving){
    direction.addEventListener('mousedown', function(e) {
      direction.style.color = "blue";
      console.log(message);
      moving = true;
    })

    direction.addEventListener('mouseup', (e) => {
      direction.style.color = "grey";
      if(moving){
        console.log('STOP!');
      }
      moving = false;
    })

    direction.addEventListener('mouseout', (e) => {
      direction.style.color = "grey";
      if(moving){ 
        console.log('STOP!');
      }
      moving = false;
    })
  }

  addEventListeners(upArrow, FORWARD, movingForward);
  addEventListeners(leftArrow, LEFT, movingLeft);
  addEventListeners(rightArrow, RIGHT, movingRight);
  addEventListeners(downArrow, BACK, movingBack);
});