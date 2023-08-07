const form = document.querySelector("form"),
fileInput = document.querySelector(".file-input"),
progressArea = document.querySelector(".progress-area"),
uploadedArea = document.querySelector(".uploaded-area");

form.addEventListener("click", () => {
    fileInput.click();
})
fileInput.onchange = ({ target }) => {
    console.log("here")
    console.log(target.files)
    all_files=target.files
//     for (let i = 0; i < all_files.length; i++) {
//         let file = target.files[i];
//         if (file) {
//             let fileName = file.name;
//             if (fileName.length >= 12) {
//                 let splitName = fileName.split('.');
//                 fileName = splitName[0].substring(0, 13) + "... ." + splitName[1];
//             }
//             uploadFile(fileName);
//         }
//       } 
}

// function uploadFile(name) {

//     let xhr = new XMLHttpRequest();
//     xhr.open("POST", "php/upload.php");
//     xhr.upload.addEventListener("progress", ({ loaded, total }) => {
//         let fileLoaded = Math.floor((loaded / total) * 100);
//         let fileTotal = Math.floor(total / 1000);
//         let fileSize;
//         (fileTotal < 1024) ? fileSize = fileTotal + " KB" : fileSize = (loaded / (1024 * 1024)).toFixed(2) + " MB";

//         let progressHTML = `<li class="row">

//     <i class="fas fa-file-alt"></i>

// <span class="name">${name} • Uploading</span>

// <span class="percent">${fileLoaded}%</span>

// <div class="progress-bar">

// <div class="progress" style="width: ${fileLoaded}%"></div>
// </div>
// </div>
// </li>`;

//         uploadedArea.classList.add("onprogress");

//         progressArea.innerHTML = progressHTML;

//         if (loaded == total) {
//             progressArea.innerHTML = "";

//             let uploadedHTML = `< li class="row" >

//                         <div class="content upload">

//                             <i class="fas fa-file-alt"></i>

//                             <span class="name">${name} • Uploaded</span>

//                             <span class="size">${fileSize}</span>

//                             <i class="fas fa-check"></i>
//                             `
//             uploadedArea.classList.remove("onprogress");

//             uploadedArea.insertAdjacentHTML("afterbegin", uploadedHTML);
//         }
//     });

//     let data = new FormData(form);
//     xhr.send(data);
// }

