var fileDrag = document.getElementById("file-drag");
var fileSelect = document.getElementById("file-upload");

fileDrag.addEventListener("dragover", fileDragHover, false);
fileDrag.addEventListener("dragleave", fileDragHover, false);
fileDrag.addEventListener("drop", fileSelectHandler, false);
fileSelect.addEventListener("change", fileSelectHandler, false);

function fileDragHover(e) {
  // prevent default behaviour
  e.preventDefault();
  e.stopPropagation();

  fileDrag.className = e.type === "dragover" ? "upload-box dragover" : "upload-box";
}

function fileSelectHandler(e) {
  // handle file selecting
  var files = e.target.files || e.dataTransfer.files;
  fileDragHover(e);
  for (var i = 0, f; (f = files[i]); i++) {
    previewFile(f);
  }
}

var imagePreview = document.getElementById("image-preview");
var uploadCaption = document.getElementById("upload-caption");
var imageDisplay = document.getElementById("image-display");
var loader = document.getElementById("loader");

function previewFile(file) {
  console.log(file.name);
  var fileName = encodeURI(file.name);

  var reader = new FileReader();
  reader.readAsDataURL(file);
  reader.onloadend = () => {
    imagePreview.src = URL.createObjectURL(file);
    imagePreview.classList.remove("hidden");
    uploadCaption.classList.add("hidden");

    displayImage(reader.result, "image-display");
  };
}

function submitImage() {
  console.log("submit");

  loader.classList.remove("hidden");
  imageDisplay.classList.add("loading");

  predictImage(imageDisplay.src);
}

function clearImage() {
  // reset selected files
  fileSelect.value = "";

  // remove preview image
  imagePreview.src = "";
  imagePreview.classList.add("hidden");
  uploadCaption.classList.remove("hidden");

  // remove result image
  imageDisplay.src = "";
  imageDisplay.classList.add("hidden");
  loader.classList.add("hidden");
}

function displayImage(image, id) {
  imageDisplay.src = image;
  imageDisplay.classList.remove("hidden");
}

function predictImage(image) {
  fetch("/predict", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(image)
  })
    .then(resp => {
      if (resp.ok)
        resp.json().then(data => {
          displayResult(data);
        });
    })
    .catch(err => {
      console.log("An error occured", err.message);
      window.alert("Failed");
    });
}

function displayResult(data) {
  // display segmentation result
  var result = document.getElementById("image-result");
  result.src = data.result;
  result.classList.remove("hidden");

  imageDisplay.classList.remove("loading");
  loader.classList.add("hidden");
  console.log(data.bbox);
}