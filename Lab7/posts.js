var parentPost = new URL(window.location.href).searchParams.get('post');
if (parentPost == null)
  parentPost = 0;
var skip = 0;
var post = {};
var display = [];
var request = new XMLHttpRequest();
var refreshTimer;

function renderPage() {
  var i = 0;
  while (i < display.length) {
    if (post.posts[i] == null || display[i] != post.posts[i]) {
      var deleteTarget = document.getElementById(display[i].id);
      if (deleteTarget.parentNode.removeChild(deleteTarget)) {
        display.splice(i, 1);
      }
    }
  }
  while (i < post.posts.length) {
    addPost(post.posts[i], 'posts');
    display.push(post.posts[i]);
    i++;
  }
}

function addPost(newPost, parent) {
  var divPosts = document.getElementById(parent);
  var divPost = document.createElement('div');
  divPost.setAttribute('id', newPost.id);
  divPost.setAttribute('class', 'post');
  divPosts.appendChild(divPost);

  if (newPost.filename.length > 1) {
    var imageDiv = document.createElement('a');
    imageDiv.setAttribute('href', 'usrimg/' + newPost.image);
    divPost.appendChild(imageDiv);
    var imageDisplay = document.createElement('img');
    imageDisplay.setAttribute('src', 'usrimg/' + newPost.image);
    imageDisplay.setAttribute('class', 'image');
    imageDiv.appendChild(imageDisplay);
  }

  var titleDiv = document.createElement('div');
  titleDiv.setAttribute('class', 'titleBlock');
  divPost.appendChild(titleDiv);

  if (newPost.title.length > 0) {
    var titleSpan = document.createElement('span');
    titleSpan.setAttribute('class', 'title');
    titleSpan.appendChild(document.createTextNode(newPost.title));
    titleDiv.appendChild(titleSpan);
  }

  var nameSpan = document.createElement('span');
  nameSpan.setAttribute('class', 'name');
  nameSpan.appendChild(document.createTextNode(newPost.name));
  titleDiv.appendChild(nameSpan);

  var timestampSpan = document.createElement('span');
  timestampSpan.setAttribute('class', 'timestamp');
  var curDate = new Date(newPost.timestamp);
  var localTimestamp = curDate.toLocaleDateString(navigator.language, {weekday: 'long'}) + ', ' + curDate.toLocaleString();
  timestampSpan.appendChild(document.createTextNode(localTimestamp));
  titleDiv.appendChild(timestampSpan);

  var idSpan = document.createElement('span');
  idSpan.setAttribute('class', 'id');
  idSpan.appendChild(document.createTextNode('No.'));
  var idA = document.createElement('a');
  idA.setAttribute('href', 'javascript:newPost(' + newPost.id + ')');
  idA.setAttribute('class', 'idLink');
  idA.appendChild(document.createTextNode(newPost.id));
  idSpan.appendChild(idA);
  titleDiv.appendChild(idSpan);
  if (parent === 'posts') {
    var reply = document.createElement('a');
    reply.setAttribute('href', 'javascript:newPost(' + newPost.id + ')');
    reply.appendChild(document.createTextNode('Reply'));
    idSpan.appendChild(document.createTextNode('['));
    idSpan.appendChild(reply);
    idSpan.appendChild(document.createTextNode(']'));
  }

  var commentDiv = document.createElement('pre');
  commentDiv.setAttribute('class', 'comment');
  commentDiv.appendChild(document.createTextNode(newPost.comment));
  divPost.appendChild(commentDiv);

  if (newPost.posts && newPost.posts.length > 0) {
    for (var childPost of newPost.posts) {
      addPost(childPost, newPost.id);
    }
  }

  if (parent === 'posts' && parentPost == 0) {
    var redirectP = document.createElement('p');
    var redirectA = document.createElement('a');
    redirectA.appendChild(document.createTextNode('Go To Post'));
    redirectA.setAttribute('href', '?post=' + newPost.id);
    redirectP.appendChild(document.createTextNode('['));
    redirectP.appendChild(redirectA);
    redirectP.appendChild(document.createTextNode(']'));
    divPost.appendChild(redirectP);
  }
}

document.forms[0].onsubmit = function(event) {
  event.preventDefault();
  var XHR = new XMLHttpRequest();
  var FD = new FormData(document.forms[0]);
  XHR.addEventListener('load', function(event) {
    var postResponse = JSON.parse(event.target.responseText);
    if (postResponse.error && postResponse.error.length > 0) {
      makeAlert('Error: ' + postResponse.error);
    } else if (postResponse.success) {
      makeAlert('Post Successful!');
      window.setTimeout(function() {
        if (document.getElementById('parent').value == 0) {
          window.location.replace('../board/?post=' + postResponse.success);
        } else {
          window.location.replace('../board/?post=' + document.getElementById('parent').value);
        }
      }, 2000);
    }
  });
  XHR.addEventListener('error', function(event) {
    makeAlert('Error: Unable to contact server.');
  });
  XHR.open('POST', 'post.cgi');
  XHR.send(FD);
  return false;
}

function makeAlert(text) {
  var alertBox = document.getElementById('alertBox');
  while (alertBox.firstChild) {
        alertBox.removeChild(alertBox.firstChild);
  }
  alertBox.appendChild(document.createTextNode(text));
  alertBox.style.display = 'block';
  window.setTimeout(function() { alertBox.style.display = 'none'; }, 5000);
}

function newPost(id) {
  document.getElementById('form').style.display = 'block';
  document.getElementById('parent').value = id;
}

function closeForm() {
  document.getElementById('form').style.display = 'none';
}

function processFile() {
  if (request.readyState != 4) {
    return;
  }
  post = JSON.parse(request.responseText);
  renderPage();
}

function getXMLFile() {
  clearTimeout(refreshTimer);
  request.open('GET', 'posts.cgi?post=' + parentPost + '&skip=' + skip, true);
  request.onreadystatechange = processFile;
  request.send();
  if (parent != 0) {
    refreshTimer = window.setTimeout(getXMLFile, 10000);
  }
}

