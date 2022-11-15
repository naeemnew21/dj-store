
function handleCredentialResponse(response) {
    console.log("Encoded JWT ID token: " + response.credential);

    const responsePayload = decodeJwtResponse(response.credential);
    console.log("email: " + responsePayload.email);
    console.log("sub: " + responsePayload.sub);
    console.log("name: " + responsePayload.name);
    console.log("img: " + responsePayload.picture);

    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/social/google_connect/", true);

    const csrftoken = getCookie('csrftoken');
    xhttp.setRequestHeader('x-csrftoken', csrftoken)
    xhttp.setRequestHeader('Content-Type', 'application/json; charset=UTF-8')
    xhttp.setRequestHeader('Accept', 'application/json')

    xhttp.onreadystatechange = function()
    {
        if (this.readyState == 4 && this.status == 200)
        {
            response = JSON.parse(this.responseText);
            console.log("response: " + response);
        }
    }
    xhttp.send(JSON.stringify({"auth_token":response.credential})); 
}


window.onload = function () {
    google.accounts.id.initialize({
    client_id: "279543566018-llpc24mgfg7ood9f3c94sl0ee65t97jk.apps.googleusercontent.com",
    callback: handleCredentialResponse
    });
    google.accounts.id.renderButton(
    document.getElementById("buttonDiv"),
    { theme: "outline", size: "large" , type: "standard"}  // customization attributes
    );
    google.accounts.id.prompt(); // also display the One Tap dialog
}

// function to decode the response.credential
function decodeJwtResponse(token) {
    var base64Url = token.split('.')[1];
    var base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    var jsonPayload = decodeURIComponent(atob(base64).split('').map(function (c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));
    return JSON.parse(jsonPayload);
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
