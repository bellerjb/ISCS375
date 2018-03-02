var word = "";
var progress = new Array(word.length);
var guessedLetters = "";
var picture = 0;
var wordbox = 0;
var animationState = 10;
var visualFrame = 8;

var framerate = 60;
var difficulty = 4;
var penalty = 15;
var totalTime = 0;
var time = totalTime;
var timer = 0;

var svgns = "http://www.w3.org/2000/svg";

function animation (state) {
  var interval = Math.round(totalTime / 7);
  if (state / interval <= visualFrame - 1) {
    visualFrame--;
    var item = (visualFrame - 8) * (-1);
    var newImg = document.getElementById("img" + item);
    newImg.style.opacity = "1";

    console.log(item)
    if (item > 1) {
      var oldImg = document.getElementById("img" + (item - 1));
      oldImg.style.opacity = "0";
    }
  }
}

function updateGuessedLetters (letter) {
  guessedLetters += letter;
}

function introAnimation () {
  switch(animationState) {
    case 10:
      sendMessage("--- BEGIN TRANSMISSION ---");
      timer = setTimeout(function(){ introAnimation(); }, 2500);
      break;
    case 9:
      sendMessage("--- SENDER: UNKNOWN ---");
      timer = setTimeout(function(){ introAnimation(); }, 2500);
      break;
    case 8:
      sendMessage("--- PRIORITY: URGENT ---");
      timer = setTimeout(function(){ introAnimation(); }, 2500);
      break;
    case 7:
      sendMessage("This is Dr. Walsh, head researcher at Station 34.");
      timer = setTimeout(function(){ introAnimation(); }, 3500);
      break;
    case 6:
      sendMessage("I am currently hiding in bunker 37-C.");
      timer = setTimeout(function(){ introAnimation(); }, 3250);
      break;
    case 5:
      sendMessage("Experiment 18-A: Chance, has evolved significantly faster than expected.");
      timer = setTimeout(function(){ introAnimation(); }, 4500);
      break;
    case 4:
      sendMessage("18-A has developed the ability to control its hosts and it is currently multiplying at a rapid pace.");
      timer = setTimeout(function(){ introAnimation(); }, 4750);
      break;
    case 3:
      sendMessage("The experiment is unsalvageable, and the bunker's walls cannot hold much longer.");
      timer = setTimeout(function(){ introAnimation(); }, 5000);
      break;
    case 2:
      sendMessage("Please, execute Emergency Procedure D.");
      timer = setTimeout(function(){ introAnimation(); }, 2000);
      break;
    case 1:
      sendSMessage("> Password Required:");
      wordbox = document.getElementById("word");
      drawWord();
      document.body.removeEventListener("keypress", skipIntro);
      timer = setInterval(function(){ tickTimer(); }, 1000 / framerate);
      document.body.addEventListener("keypress", handleGuess);
      break;
    default:
      throw "Invalid Animation State";
  }
  animationState--;
}

function skipIntro (event) {
  while (animationState > 0) {
    introAnimation();
  }
}

function drawWord () {
  for (i = 0; i < word.length; i++) {
    var letterNode = document.createTextNode("");
    var letterBox = document.createElement("div");
    letterBox.appendChild(letterNode);

    letterBox.setAttribute("class", "letter");

    wordbox.appendChild(letterBox);
  }
}

function handleGuess (event) {
  var letter = String.fromCharCode(event.which).toUpperCase();
  if (guessedLetters.includes(letter)) {
    return;
  }

  updateGuessedLetters(letter);

  var found = false;
  for (i = 0; i < word.length; i++) {
    if (letter == word[i]) {
      found = true;
      drawLetter(i);
    }
  }

  if (found != true) {
    time -= penalty;
    sendMessage("ERROR: Letter \"" + letter.toUpperCase() + "\" not found.");
  }

  if (checkWin()) {
    winGame();
  }
}

function sendMessage (message) {
  messageText = document.createTextNode(message);
  messageBox = document.createElement("div");
  messageBox.appendChild(messageText);
  messageBox.setAttribute("class", "message");

  log = document.getElementById("log");
  log.prepend(messageBox);
}

function sendSMessage (message) {
  messageText = document.createTextNode(message);
  messageItalic = document.createElement("i");
  messageItalic.appendChild(messageText);
  messageBox = document.createElement("div");
  messageBox.appendChild(messageItalic);
  messageBox.setAttribute("class", "message");

  log = document.getElementById("log");
  log.prepend(messageBox);
}

function loadGame () {
  word = pickWord();
  totalTime = word.length * difficulty * framerate;
  time = totalTime;
  penalty = Math.round(totalTime / penalty);
  picture = document.getElementById("main");
  document.body.addEventListener("keypress", skipIntro);
  introAnimation();
}

function pickWord () {
  var selection = Math.floor(Math.random() * words.length);
  return words[selection].toUpperCase();
}

function tickTimer () {
  var passed = totalTime - time;
  var progress = passed / totalTime;
  var progressBar = document.getElementById("timer");

  progressBar.style.width = progress * 100 + "%";
  if (time % 10 == 0) {
    animation(time);
  }

  if (time <= 0) {
    loseGame();
  } else {
    time--;
  }
}

function loseGame () {
  clearInterval(timer);
  document.getElementById("timer").style.width = "100%";
  resetGame();
  for (i = 0; i < word.length; i++) {
    if (progress[i] != word[i]) {
      var letterNode = document.createTextNode(word[i]);
      var boldLetter = document.createElement("b");
      boldLetter.appendChild(letterNode);
      var letterBox = wordbox.childNodes[i];
      letterBox.appendChild(boldLetter);
    }
  }
  sendMessage("The door ha");
  setTimeout(function(){ killSignal(); }, 3000);
}

function winGame () {
  clearInterval(timer);
  resetGame();
  sendSMessage("> Password: \"" + word + "\" accepted.");
  setTimeout(function(){ sendSMessage("> Launch Successful."); }, 2000);
  setTimeout(function(){ killSignal(); }, 3000);
}

function killSignal () {
  for (var i = 1; i < 8; i++) {
    document.getElementById("img" + i).style.opacity = 0;
  }
  setTimeout(function(){ sendMessage("--- TRANSMISSION LOST ---"); }, 2000);
}

function resetGame () {
  document.body.removeEventListener("keypress", handleGuess);

  var guessbox = wordbox.parentElement;
  guessbox.setAttribute("class", guessbox.className + " disabled");
  var letters = wordbox.children;
  for (var i = 0; i < letters.length; i++) {
    letters[i].setAttribute("class", letters[i].className + " disabled");
  }
  for (var i = 0; i < letters.length; i++) {
    if (progress[i] == word[i]) {
      letters[i].style.border = "none";
    }
  }
}

function drawLetter (i) {
  var letter = word[i];
  progress[i] = word[i];
  var letterNode = document.createTextNode(letter);
  var letterBox = wordbox.childNodes[i];
  letterBox.appendChild(letterNode);
}

function checkWin () {
  for (i = 0; i < word.length; i++) {
    if (guessedLetters.includes(word[i]) == false) {
      return false;
    }
  }
  return true;
}

