
let password = document.getElementById('password')
let confrimPassword = document.getElementById('confirm_password')


function validateInput(input) {
    if (input.value == '') {
        input.classList.remove('is-valid')
        input.classList.add('is-invalid')
    } else {
        input.classList.remove('is-invalid')
        input.classList.add('is-valid')
    }
}

function confrimPasswordValidation() {
    if (confrimPassword.value != password.value) {
        confrimPassword.classList.remove('is-valid')
        confrimPassword.classList.add('is-invalid')
    } else {
        confrimPassword.classList.remove('is-invalid')
        confrimPassword.classList.add('is-valid')
    }
}

function submit(form) {
    fetch().then(res=>{
        let myData = res.json();
        return myData
    })
}

