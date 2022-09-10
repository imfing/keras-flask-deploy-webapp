//========================================================================
// Drag and drop image handling
//========================================================================
function handleFiles(event) {
    var files = event.target.files;
    $("#src").attr("src", URL.createObjectURL(files[0]));
    document.getElementById("audio").load();
    document.getElementById("audio-play").style.display = "block";
}

document.getElementById("file-upload").addEventListener("change", handleFiles, false);

var fileDrag = document.getElementById("file-drag");
var fileSelect = document.getElementById("file-upload");

// Add event listeners
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

//========================================================================
// Web page elements for functions to use
//========================================================================
var fileSuccess = document.getElementById("was-success");
var forthissong = document.getElementById("forthissong");
var justopinion = document.getElementById("justopinion");
var spinner = document.getElementById("spinner")
var imagePreview = document.getElementById("image-preview");
var imageDisplay = document.getElementById("image-display");
var uploadCaption = document.getElementById("upload-caption");
var predResult = document.getElementById("pred-result");
// var loader = document.getElementById("loader");

//========================================================================
// Main button events
//========================================================================
function submitAudio() {
    // action for the submit button
    console.log("submit");

    // call the predict function of the backend
    if (globFile !== null) {
        if (globFile.type.split('/')[0] == 'audio') {
            // document.getElementById("file-info").style.display = "inline-block";
            hide(fileSuccess)
            show(spinner)
            predictAudio(globFile);
            console.log(document.getElementById('file-upload').value)
        } else {
            window.alert("Invalid File Type. Please submit an audio file");
        }
    } else {
        window.alert("Please upload a .wav file before submitting");
    }

}

function clearAudio() {
    // reset selected files
    fileSelect.value = "";

    // remove image sources and hide them
    imagePreview.src = "";
    imageDisplay.src = "";
    predResult.innerHTML = "";

    globFile = null

    hide(imagePreview);
    hide(imageDisplay);
    // hide(loader);
    hide(predResult);
    show(uploadCaption);
    show(willhetext)
    justopinion.textContent = ""
    hide(justopinion)
    hide(forthissong)
    hide(fileSuccess)
    imageDisplay.classList.remove("loading");
    document.getElementById("audio-play").style.display = "none";
    // document.getElementById("file-info").style.display = "none";


}

function previewFile(file) {
    // show the preview of the image
    console.log(file)
    globFile = file;
    console.log(file.name);
    var fileName = encodeURI(file.name);
    // console.log()
    var reader = new FileReader();
    imagePreview.innerText = fileName;
    show(imagePreview);
    hide(uploadCaption);
    show(fileSuccess)
    hide(willhetext)

}

var globFile = null;

//========================================================================
// Helper functions
//========================================================================

function predictAudio(file) {
    // console.log(image.blob)
    var form = new FormData();
    form.append('audio_file', file, "poopy.wav")
    // "Content-Type": "multipart/form-data"
    fetch("/predict", {
        method: "POST",
        headers: {},
        body: form
    })
        .then(resp => {
            if (resp.ok)
                resp.json().then(data => {
                    displayResult(data);
                });
        })
        .catch(err => {
            console.log("An error occured", err.message);
            window.alert("Oops! Something went wrong.");
        });
}

function showFileInfo() {
    document.getElementById('file-upload').value

}

function displayResult(data, errors) {
    // display the result
    imageDisplay.classList.remove("loading");
    console.log(data)

    // hide(loader);
    // predResult.innerHTML = data.result;
    show(predResult);
    var string = data.emotion[0]
    hide(spinner)
    var div = document.getElementById('justopinion');
    // 01 = neutral, 02 = calm, 03 = happy, 04 = sad, 05 = angry, 06 = fearful, 07 = disgust, 08 = surprised
    if (string.includes('neutral')) {
        imageDisplay.src = './static/' + 'neutral' + '.png'
        div.textContent = "neutral";
    } else if (string.includes('calm')) {
        // imageDisplay.src = './static/' + 'calm' + '.png'
        // div.textContent = "calm";
        imageDisplay.src = './static/' + 'surprised' + '.png'
        div.textContent = "surprised";
    } else if (string.includes('happy')) {
        imageDisplay.src = './static/' + 'happy' + '.png'
        div.textContent = "happy";
    } else if (string.includes('sad')) {
        imageDisplay.src = './static/' + 'sad' + '.png'
        div.textContent = "sad";
    } else if (string.includes('angry')) {
        imageDisplay.src = './static/' + 'angry' + '.png'
        div.textContent = "angry";
    } else if (string.includes('fearful')) {
        imageDisplay.src = './static/' + 'fearful' + '.png'
        div.textContent = "fearful";
    } else if (string.includes('disgust')) {
        imageDisplay.src = './static/' + 'disgust' + '.png'
        div.textContent = "disgusted";
    } else if (string.includes('surprised')) {
        imageDisplay.src = './static/' + 'surprised' + '.png'
        div.textContent = "surprised";
    } else {
        imageDisplay.src = './static/' + 'confused' + '.png'
        div.textContent = "?";
    }

    if (imageDisplay.classList.contains('hidden')) {
        show(imageDisplay)
    }

    show(justopinion)
    show(forthissong)

}

function hide(el) {
    // hide an element
    el.classList.add("hidden");
}

function show(el) {
    // show an element
    el.classList.remove("hidden");
}