let firstnameError = document.getElementById('first_name_error');
let lastnameError = document.getElementById('last_name_error');
let phonenoError = document.getElementById('phone_no_error');
let emailError = document.getElementById('email_error');
let passwordError = document.getElementById('password_error');


function validateFName() {
    let fname = document.getElementById('first_name');
    let nameRegex = /^[A-Za-z]+$/;

    fname.addEventListener('input', function () {
        if (!nameRegex.test(fname.value)) {
            fname.value = fname.value.replace(/[^A-Za-z]/g, '');
            firstnameError.innerHTML = 'Only alphabets are allowed';
        } else {
            firstnameError.innerHTML = '';
        }
    });

    if (fname.value.length === 0) {
        firstnameError.innerHTML = 'First Name is required';
        return false;
    } else if (fname.value.length < 3) {
        firstnameError.innerHTML = 'First Name should be at least 3 characters';
        return false;
    } else {
        firstnameError.innerHTML = '<i class="fa-solid fa-circle-check"></i>';
        return true;
    }
}

function validateLName() {
    let lname = document.getElementById('last_name');
    let nameRegex = /^[A-Za-z]+$/;

    lname.addEventListener('input', function () {
        if (!nameRegex.test(lname.value)) {
            lname.value = lname.value.replace(/[^A-Za-z]/g, '');
            lastnameError.innerHTML = 'Only alphabets are allowed';
        } else {
            lastnameError.innerHTML = '';
        }
    });

    if (lname.value.length === 0) {
        lastnameError.innerHTML = 'Last Name is required';
        return false;
    } else if (lname.value.length < 3) {
        lastnameError.innerHTML = 'Last Name should be at least 3 characters';
        return false;
    } else {
        lastnameError.innerHTML = '<i class="fa-solid fa-circle-check"></i>';
        return true;
    }
}

function validatePhone() {
    let phone = document.getElementById('phone_no');
    let phoneRegex = /^\d{11}$/;

    phone.addEventListener('input', function () {
        phone.value = phone.value.replace(/\D/g, ''); // Remove non-numeric characters
        if (phone.value.length > 11) {
            phone.value = phone.value.slice(0, 11); // Limit to 11 digits
        }
        phonenoError.innerHTML = phoneRegex.test(phone.value) ? '' : 'Phone no should be exactly 11 digits';
    });

    if (phone.value.length === 0) {
        phonenoError.innerHTML = 'Phone no is required';
        return false;
    } else if (!phoneRegex.test(phone.value)) {
        phonenoError.innerHTML = 'Phone no should be exactly 11 digits';
        return false;
    } else {
        phonenoError.innerHTML = '<i class="fa-solid fa-circle-check"></i>';
        return true;
    }
}

function validateEmail() {
    let email = document.getElementById('email');
    let emailError = document.getElementById('email_error');

    // Strictly allow only ".com" domains
    let emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.com$/;

    email.addEventListener('input', function () {
        email.value = email.value.replace(/^[^a-zA-Z]+/, ''); // Remove invalid starting characters

        if (!emailRegex.test(email.value)) {
            emailError.innerHTML = 'Enter a valid email (e.g., example@gmail.com)';
        } else {
            emailError.innerHTML = '';
        }
    });

    if (email.value.trim() === '') {
        emailError.innerHTML = 'Email is required';
        return false;
    } else if (!emailRegex.test(email.value.trim())) {
        emailError.innerHTML = 'Enter a valid email (e.g., example@gmail.com)';
        return false;
    } else {
        emailError.innerHTML = '<i class="fa-solid fa-circle-check"></i>';
        return true;
    }
}


function validatePassword() {
  let password = document.getElementById('password');
  let passwordError = document.getElementById('password_error');

  // Remove spaces from the password input
  password.addEventListener('input', function () {
      password.value = password.value.replace(/\s/g, ''); // Removes all spaces
  });

  if (password.value.length === 0) {
      passwordError.innerHTML = 'Password is required';
      return false;
  } else if (password.value.length < 6) {
      passwordError.innerHTML = 'Password should be at least 6 characters long';
      return false;
  } else {
      passwordError.innerHTML = '<i class="fa-solid fa-circle-check"></i>';
      return true;
  }
}


function validateForm() {
    let isFNameValid = validateFName();
    let isLNameValid = validateLName();
    let isPhoneValid = validatePhone();
    let isEmailValid = validateEmail();
    let isPasswordValid = validatePassword();

    return isFNameValid && isLNameValid && isPhoneValid && isEmailValid && isPasswordValid;
}

function togglePassword(inputId, showIconId, hideIconId) {
    const passwordField = document.getElementById(inputId);
    const showIcon = document.getElementById(showIconId);
    const hideIcon = document.getElementById(hideIconId);

    if (passwordField.type === "password") {
        passwordField.type = "text"; // Show password
        showIcon.style.display = "none";
        hideIcon.style.display = "block";
    } else {
        passwordField.type = "password"; // Hide password
        showIcon.style.display = "block";
        hideIcon.style.display = "none";
    }
}
