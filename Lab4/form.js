var num_posts = 0;

function submit_form () {
  var myDate = new Date();
  var comment, commentP;

  comment = sanitize(document.getElementById("comment_box").value);
  commentP = document.createElement("p");
  timeS = document.createElement("span");
  timeS.appendChild(document.createTextNode(myDate.toString()));
  timeS.setAttribute("class", "timestamp");

  commentP.appendChild(timeS);
  commentP.appendChild(document.createElement("br"));
  commentP.appendChild(document.createTextNode(comment));
  commentP.setAttribute("class", "comment");
  document.getElementById("comments").appendChild(commentP);
  document.getElementById("comments").appendChild(document.createElement("br"));

  num_posts++;
  if (num_posts == 1) {
    document.getElementById("num_posts").innerHTML = "Post tracker: Only one comment";
  } else {
    document.getElementById("num_posts").innerHTML = "Post tracker: " + num_posts + " comments.";
  }
}

function sanitize (text) {
  var output = "";
  for (var i = 0; i < text.length; i++) {
    var letter = text[i].charCodeAt();
    if ((letter > 47 && letter < 58) || (letter > 64 && letter < 91) || (letter > 96 && letter < 123) || (letter == 32)) {
      output += text[i];
    }
  }
  return output;
}

function glitterSubmitForm () {
  var myDate = new Date();
  var commentText, comment, infoBox, time, timeStamp, username, usernameBox, icon, userIcon;

  commentText = safeSanitize(document.getElementById("commentBox").value);
  if (commentText == "") {
    return;
  }
  time = "" + myDate.getHours() + ":" + myDate.getMinutes();
  username = safeSanitize(document.getElementById("name").value);
  if (username == "") {
    username = "No Username";
  }
  icon = document.getElementById("icon").files[0];

  comment = document.createElement("div");
  comment.setAttribute("class", "comment");
  comment.appendChild(document.createTextNode(commentText));

  infoBox = document.createElement("div");
  infoBox.setAttribute("class", "info");

  timeStamp = document.createElement("span");
  timeStamp.appendChild(document.createTextNode(time));
  timeStamp.setAttribute("class", "timestamp");
  infoBox.prepend(timeStamp);

  usernameBox = document.createElement("span");
  usernameBox.appendChild(document.createTextNode(username));
  usernameBox.setAttribute("class", "username");
  infoBox.prepend(usernameBox);

  comment.prepend(infoBox);

  userIcon = document.createElement("img");
  var reader  = new FileReader();
  reader.onloadend = function () { userIcon.src = reader.result; };
  if (icon) {
    reader.readAsDataURL(icon);
  } else {
    userIcon.src = "icon.svg";
  }
  userIcon.setAttribute("class", "icon");
  comment.prepend(userIcon);

  document.getElementById("comments").appendChild(comment);

  num_posts++;
  document.getElementById("numPosts").innerHTML = "(" + num_posts + ")";
  document.getElementById("commentCount").innerHTML = (num_posts == 1 ? "One Comment " : "All Comments ") + document.getElementById("numPosts").outerHTML;
  if (num_posts == 1) {
    document.getElementById("numPosts").style.display = "none";
  } else {
    document.getElementById("numPosts").style.display = "inline";
  }
}

function previewFile () {
  // https://stackoverflow.com/a/34178498
  var preview = document.getElementById("preview");
  var file = document.getElementById("icon").files[0];
  var reader  = new FileReader();

  reader.onloadend = function () {
    preview.src = reader.result;
  }

  if (file) {
    reader.readAsDataURL(file);
  } else {
    preview.src = "";
  }
}

// Added period character
function safeSanitize (text) {
  var output = "";
  for (var i = 0; i < text.length; i++) {
    var letter = text[i].charCodeAt();
    if ((letter > 47 && letter < 58) || (letter > 64 && letter < 91) || (letter > 96 && letter < 123) || (letter == 32) || (letter == 46)) {
      output += text[i];
    }
  }
  return output;
}

