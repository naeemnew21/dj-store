
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


  // button.addEventListener('click', () => {
  //   let prodName = document.getElementById('product_name')
  //   let prodPrice = document.getElementById('price')
  //   let size1 = document.getElementById('size1')
  //   let size2 = document.getElementById('size2')
  //   let size3 = document.getElementById('size3')
  //   let size4 = document.getElementById('size4')
  //   let size5 = document.getElementById('size5')
  //   let size6 = document.getElementById('size6')
  //   let color1 = document.getElementById('color1')
  //   let color2 = document.getElementById('color2')
  //   let color3 = document.getElementById('color3')
  //   let color4 = document.getElementById('color4')
  //   let color5 = document.getElementById('color5')
  //   let fileUpload = document.getElementById('file-uploader').files[0]
  //   let desc = document.getElementById('description')
  //   let formData = {
  //     category:'T-Shirt',
  //     brand:'zara',
  //     name: prodName.value,
  //     suitable: "all",
  //     color1:color1.checked ? "black"  : "",
  //     color2:color2.checked? "white"  : "",
  //     color3:color3.checked? "red"  : "",
  //     color4:color4.checked? "blue"  : "",
  //     color5:color5.checked? "green"  : "",
  //     size1:size1.checked? "xs"  : "",
  //     size2:size2.checked? "s"  : "",
  //     size3:size3.checked? "m"  : "",
  //     size4:size4.checked? "l"  : "",
  //     size5:size5.checked? "xl"  : "",
  //     size6:size6.checked? "xxl"  : "",
  //     quantity:count.value,
  //     price: prodPrice.value,
  //     price_dis:'1',
  //     main_image:fileUpload,
  //     details:desc.value
  //   }
  //   console.log(formData)
  //   fetch('/add-product',{
  //     method:'POST',
  //     body:formData,
  //     headers: {
  //     //   'Content-Type': 'multipart/form-data', 
  //     //   'Accept': 'application/json',
  //       'X-CSRFToken': getCookie('csrftoken')
  //     },
  //   }).then(x => x.json()).then(res => {console.log(res)})
  // })
 })(window);



 function add_product()
{   
    let prodName = document.getElementById('product_name')
    let prodPrice = document.getElementById('price')
    let size1 = document.getElementById('size1')
    let size2 = document.getElementById('size2')
    let size3 = document.getElementById('size3')
    let size4 = document.getElementById('size4')
    let size5 = document.getElementById('size5')
    let size6 = document.getElementById('size6')
    let color1 = document.getElementById('color1')
    let color2 = document.getElementById('color2')
    let color3 = document.getElementById('color3')
    let color4 = document.getElementById('color4')
    let color5 = document.getElementById('color5')
    let fileUpload = document.getElementById('file-uploader').files[0]
    let desc = document.getElementById('description')
    
    formData = new FormData();
    formData.append("category", 'T-Shirt');
    formData.append("brand", 'zara');
    formData.append("name", prodName.value);
    formData.append("suitable", "all");
    formData.append("color1", color1.checked ? "black"  : "");
    formData.append("color2", color2.checked? "white"  : "");
    formData.append("color3", color3.checked? "red"  : "");
    formData.append("color4", color4.checked? "blue"  : "");
    formData.append("color5", color5.checked? "green"  : "");
    formData.append("size1", size1.checked? "xs"  : "");
    formData.append("size2", size2.checked? "s"  : "");
    formData.append("size3", size3.checked? "m"  : "");
    formData.append("size4", size4.checked? "l"  : "");
    formData.append("size5", size5.checked? "xl"  : "");
    formData.append("size6", size6.checked? "xxl"  : "");
    formData.append("quantity", count.value);
    formData.append("price", prodPrice.value);
    formData.append("price_dis", "1");
    formData.append("details", desc.value);
    formData.append("main_image", fileUpload);


    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/add-product", true);

    const csrftoken = getCookie('csrftoken');
    xhttp.setRequestHeader('x-csrftoken', csrftoken)
    // xhttp.setRequestHeader('Content-Type', 'multipart/form-data')
    // xhttp.setRequestHeader('Accept', 'application/json')

    xhttp.onreadystatechange = function()
    {
      if (this.readyState == 4 && this.status == 200)
      {
        response = JSON.parse(this.responseText);
        console.log(response);
      }
    }

    xhttp.send(formData);   
}  




function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}