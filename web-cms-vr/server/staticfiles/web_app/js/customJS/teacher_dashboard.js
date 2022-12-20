const temporary = document.getElementById('temporary');
const accepting = document.getElementById('accepting');
const ready = document.getElementById('ready');
const started = document.getElementById('started');
const assessed = document.getElementById('assessed');
const published = document.getElementById('published');
const targetURL = "/web_app/teacher/filter_exhibitions/?filter=";

temporary.addEventListener("click", filter);
accepting.addEventListener("click", filter);
ready.addEventListener("click", filter);
started.addEventListener("click", filter);
assessed.addEventListener("click", filter);
published.addEventListener("click", filter);

function filter() {
  if (this === temporary) {
    //console.log("Temporary Stored");
    window.location.href = targetURL + "Temporary Stored";
  } else if (this === accepting) {
    //console.log(targetURL + "Accepting Artworks" + "'");
    window.location.href = targetURL + "Accepting Artworks";
  } else if (this === ready) {
    //console.log("Ready to be Assessed");
    window.location.href = targetURL + "Ready to be Assessed";
  } else if (this === started) {
    //console.log("Assessment Started");
    window.location.href = targetURL + "Assessment Started";
  } else if (this === assessed) {
    //console.log("Assessed");
    window.location.href = targetURL + "Assessed";
  } else if (this === published) {
    //console.log("Published");
    window.location.href = targetURL + "Published";
  }
}