(function (window, undefined) {
  'use strict';
  let fileUpload = document.getElementById('file-uploader');
  let previewImg = document.getElementById('preview');
  let button = document.getElementById('send-data')
  fileUpload.addEventListener('change', (e) => {
    if (e.target.files[0]) previewImg.classList.remove('d-none');
    previewImg.src = URL.createObjectURL(e.target.files[0]);
  });
  console.log(button)
})(window);


