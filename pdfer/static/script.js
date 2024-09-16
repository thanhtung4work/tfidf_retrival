function uploadDocument() {
    // Get HTML Element
    const fileUpload    = document.getElementById("fileInput")
    const uploadStatus  = document.getElementById("uploadStatus")
    
    // Check select file
    if (!fileUpload.files.length) {
        uploadStatus.textContent = "Select a file to upload!"
        return
    }

    const file = fileUpload.files[0]
    const formData = new FormData();
    formData.append("file", file)

    // Call upload API
    fetch("/documents/upload", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            uploadStatus.textContent = `Error: ${data.error}`
        } else {
            uploadStatus.textContent = `Success: ${data.message}`
            listFiles()
        }
    })
    .catch(error => {
        uploadStatus.textContent = `Error: ${error.message}`
    });
}

function extractText() {
    const queryInput = document.getElementById('queryInput')
    const extractStatus = document.getElementById('extractStatus')
    const resultsList = document.getElementById('resultsList')

    const query = queryInput.value;
    if (!query) {
        extractStatus.textContent = 'Please enter a query.'
        return
    }
    
    extractStatus.textContent = 'Processing, please wait...'

    fetch('/extract', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
    })
    .then(response => response.json())
    .then(data => {
        resultsList.innerHTML = ''
        if (data.error) {
            extractStatus.textContent = `Error: ${data.error}`
        } else {
            extractStatus.textContent = 'Extraction completed successfully. See results below:'
            // Object.entries(data).sort(([,a],[,b]) => a-b)
            for (const [file, score] of Object.entries(data).sort(([,a],[,b]) => a-b).reverse()) {
                const li = document.createElement('li')
                
                // Download button
                const downloadButton = document.createElement('button')
                downloadButton.textContent = 'Download'
                downloadButton.onclick = () => downloadFile(file)
                
                li.appendChild(downloadButton)
                
                //Text content
                const textSpan = document.createElement('span')
                textSpan.textContent = `[${score.toFixed(4)}] ${file}`
                li.appendChild(textSpan)

                resultsList.appendChild(li)
            }
        }
    })
    .catch(error => {
        extractStatus.textContent = `Error: ${error.message}`
    })
}

function listFiles() {
    const fileList = document.getElementById("fileList")
    fileList.innerHTML = ""

    fetch("/documents", {method: "POST"})
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            fileList.innerHTML = `<li> Error: ${data.error}</li>`
        }
        else {
            data.documents.forEach(file => {
                const li = document.createElement('li')
                for (const item of ['card', 'col-3']){
                    li.classList.add(item)
                }
                
                const div = document.createElement('div')
            
                // Download button
                const downloadButton = document.createElement('button')
                downloadButton.textContent = 'Download'
                downloadButton.onclick = () => downloadFile(file)
                
                div.appendChild(downloadButton)

                // Remove button
                const removeButton = document.createElement('button')
                removeButton.classList.add("negative-btn")
                removeButton.textContent = 'Remove'
                removeButton.onclick = () => removeFile(file)

                div.appendChild(removeButton)
                
                // Text content
                const textTag = document.createElement("span")
                textTag.textContent = file

                li.appendChild(textTag)
                li.appendChild(div)

                fileList.appendChild(li)
            });
        }
    })
    .catch(error => {
        fileList.innerHTML = `<li>Error: ${error.message}</li>`;
    });
}

// Function to download a file
function downloadFile(filename) {
    window.location.href = `/documents/download/${filename}`;
}

// Function to remove file
function removeFile(filename) {
    fetch(`/documents/remove/${filename}`, {
        method: "DELETE"
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message || data.error)
        listFiles()
    })
    .catch(error => {
        alert(`Error: ${error.message}`)
    })
}
