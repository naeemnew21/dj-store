function add_to_cart(element)
{
  let added = document.getElementById(`added-${element.id}`)
    let data = {};
    data['product']  = element.id;
    data['action']   = element.name;
    data['quantity'] = 1
    
    let xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/en/cart/cart-api", true);
    const csrftoken = getCookie('csrftoken');
    xhttp.setRequestHeader('x-csrftoken', csrftoken)
    xhttp.setRequestHeader('Content-Type', 'application/json; charset=UTF-8')
    xhttp.setRequestHeader('Accept', 'application/json')
    xhttp.onreadystatechange = function()
    {
      if (this.readyState == 4 && this.status == 201)
      {
        response = JSON.parse(this.responseText)
        document.getElementById("my_cart").innerHTML = response.my_cart;
      }
    }
    xhttp.send(JSON.stringify(data));
    element.classList.add('d-none')
    added.classList.add('d-block')
    added.classList.add('added-color')
}


function add_to_cart_cart_page(element)
{
    let data = {};
    data['product']  = element.id;
    data['action']   = element.name;
    data['quantity'] = 1
    let xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/en/cart/cart-api", true);
    const csrftoken = getCookie('csrftoken');
    xhttp.setRequestHeader('x-csrftoken', csrftoken)
    xhttp.setRequestHeader('Content-Type', 'application/json; charset=UTF-8')
    xhttp.setRequestHeader('Accept', 'application/json')

    xhttp.onreadystatechange = function()
    {
      if (this.readyState == 4 && this.status == 201)
      {
        response = JSON.parse(this.responseText)
        pk = response.order_id;
        document.getElementById("my_cart").innerHTML = response.my_cart;
        document.getElementById("price-"+ pk).innerHTML = response.order_price;
        document.getElementById("total_before").innerHTML = response.total;
        document.getElementById("total_after").innerHTML = response.totch;
      }
    }
    
    xhttp.send(JSON.stringify(data));   
}


function add_quant_to_cart(element)
{
    let data = {};
    data['product']  = element.id;
    data['action']   = element.name;
    data['quantity'] = document.getElementById("product_quantity_cart").value
    
    let xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/en/cart/cart-api", true);
    const csrftoken = getCookie('csrftoken');
    xhttp.setRequestHeader('x-csrftoken', csrftoken)
    xhttp.setRequestHeader('Content-Type', 'application/json; charset=UTF-8')
    xhttp.setRequestHeader('Accept', 'application/json')

    xhttp.onreadystatechange = function()
    {
      if (this.readyState == 4 && this.status == 201)
      {
        response = JSON.parse(this.responseText)
        document.getElementById("my_cart").innerHTML = response.my_cart;
      }
    }
    
    xhttp.send(JSON.stringify(data));   
}

function del_order(element)
{
    pk = element.id;
    let xhttp = new XMLHttpRequest();
    xhttp.open("DELETE", "/en/cart/del-order/"+pk, true);
    const csrftoken = getCookie('csrftoken');
    xhttp.setRequestHeader('x-csrftoken', csrftoken)
    xhttp.setRequestHeader('Content-Type', 'application/json; charset=UTF-8')
    xhttp.setRequestHeader('Accept', 'application/json')

    xhttp.onreadystatechange = function()
    {
      if (this.status == 204)
      {
        location.reload()
      }
    }
    xhttp.send();   
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
