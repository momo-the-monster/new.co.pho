var fileInput = document.getElementById('capture');
fileInput.addEventListener('change', (e) => processImage(e.target.files));

// Get display elements
var captureButton = document.getElementById('capture-button')
var output = document.getElementById('output');
var loading = document.getElementById('loading')

loading.style.display = 'none';

function processImage(fileList) {
    var file = null;

    for (var i = 0; i < fileList.length; i++) {
        if (fileList[i].type.match(/^image\//)) {
            file = fileList[i];
            break;
        }
    }

    var url = '/upload';
    var formData = new FormData();
    formData.append('file', file);

    loading.style.display = 'initial';
    captureButton.style.display = 'none';

    fetch(url, {
        method: 'POST',
        body: formData,
    }).then(response => {
        response.json().then(function (json) {
            output.src = 'http://' + json.url;
            loading.style.display = 'none';
        });
    });
}