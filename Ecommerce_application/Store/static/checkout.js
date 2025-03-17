document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('checkoutform');
    form.addEventListener('submit', function (event) {
        if (!validateForm()) {
            event.preventDefault(); 
        }
    });
});

function validateForm() {
    let isValid = true;
    if (!validateF_name()) {
        isValid = false;
    }
    if (!validateL_name()) {
        isValid = false;
    }
    if (!validatePhone()) {
        isValid = false;
    }
    if (!validateEmail()) {
        isValid = false;
    }
    if (!validateAddress()) {
        isValid = false;
    }
    if (!validateCity()) {
        isValid = false;
    }
    if (!validateZipcode()) {
        isValid = false;
    }

    return isValid;
}

function validateF_name() {
    const nameInput = document.getElementById('first_name');
    const nameError = document.getElementById('first_name_error');
    const fname = nameInput.value.trim();

    nameError.textContent = '';

    if (fname.length === 0) {
        nameError.textContent = 'First name is required';
        return false;
    }

    if (fname.length < 3) {
        nameError.textContent = 'First Name should be at least 3 characters.';
        return false;
    }

    if (fname.length > 15) {
        nameError.textContent = 'First Name cannot exceed 15 characters.';
        return false;
    }

    if (!/^[A-Za-z]+( [A-Za-z]+)*$/.test(fname)) {
        nameError.textContent = 'Only alphabets and single spaces are allowed';
        return false;
    }

    return true;
}

function validateL_name() {
    const nameInput = document.getElementById('last_name');
    const nameError = document.getElementById('last_name_error');
    const lname = nameInput.value.trim();

    nameError.textContent = '';

    if (lname.length === 0) {
        nameError.textContent = 'Last name is required';
        return false;
    }

    if (lname.length < 3) {
        nameError.textContent = 'Last Name should be at least 3 characters.';
        return false;
    }

    if (lname.length > 15) {
        nameError.textContent = 'Last Name cannot exceed 15 characters.';
        return false;
    }
    if (!/^[A-Za-z]+( [A-Za-z]+)*$/.test(lname)) {
        nameError.textContent = 'Only alphabets and single spaces are allowed';
        return false;
    }

    return true;
}

document.getElementById('phone_no').addEventListener('input', function() {
    this.value = this.value.replace(/[^0-9]/g, '');  
});

function validatePhone() {
    const phoneInput = document.getElementById('phone_no');
    const phoneError = document.getElementById('phone_no_error');
    const phone = phoneInput.value.trim();

    phoneError.textContent = '';  

    if (phone.length === 0) {
        phoneError.textContent = 'Phone number is required.';
        return false;
    }

    if (!/^03\d{9}$/.test(phone)) {
        phoneError.textContent = 'Phone number must start with "03" and be 11 digits.';
        return false;
    }

    return true;
}

function validateEmail() {
    const email = document.getElementById('email').value.trim();
    const emailError = document.getElementById('email_error');
    emailError.textContent = ''; 

    if (email.length === 0) {
        emailError.textContent = 'Email is required';
        return false;
    }
    if (email.length > 30) {
        emailError.textContent = 'Email cannot exceed 30 characters.';
        return false;
    }
    const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
    if (!emailPattern.test(email)) {
        emailError.textContent = 'Enter a valid email like example@gmail.com';
        return false;
    }
    return true;
}

function validateAddress() {
    const addressInput = document.getElementById('address');
    const addressError = document.getElementById('address_error');
    const address = addressInput.value.trim();
    addressError.textContent = ''; // Clear previous error

    if (address.length === 0) {
        addressError.textContent = 'Address is required';
        return false;
    }
    if (address.length > 40) {
        addressError.textContent = 'Address cannot exceed 40 characters';
        return false;
    }
    if (/[^a-zA-Z0-9\s,.\-\/]/.test(address)) {
        addressError.textContent = 'Invalid characters detected. Only letters, numbers, spaces, commas, periods, hyphens, and slashes are allowed.';
        return false;
    }
    return true;
}

document.getElementById('city').addEventListener('input', function() {
    this.value = this.value.replace(/[^A-Za-z ]/g, '');  
});

function validateCity() {
    const cityInput = document.getElementById('city');
    const cityError = document.getElementById('city_error');
    const cityname = cityInput.value.trim();
    cityError.textContent = ''; // Clear previous error

    if (cityname.length === 0) {
        cityError.textContent = 'City is required';
        return false;
    }
    if (cityname.length > 25) {
        cityError.textContent = 'City name cannot exceed 25 characters';
        return false;
    }

    // Updated regex to disallow numbers
    if (!/^[A-Za-z]+( [A-Za-z]+)*$/.test(cityname)) {
        cityError.textContent = 'Only alphabets and single spaces are allowed';
        return false;
    }

    return true;
}



document.addEventListener('DOMContentLoaded', function() {
    const zipInput = document.getElementById('pincode');
    const zipError = document.getElementById('pincode_error');
    
    // Restrict non-numeric characters in the zip code field
    zipInput.addEventListener('input', function() {
        this.value = this.value.replace(/[^0-9]/g, ''); // Only digits are allowed
    });

    zipInput.addEventListener('blur', function() {
        validateZipcode(); // Validate when the field loses focus
    });
});
document.addEventListener('DOMContentLoaded', function() {
    const zipInput = document.getElementById('pincode');
    const zipError = document.getElementById('pincode_error');
    
    // Restrict non-numeric characters in the zip code field
    zipInput.addEventListener('input', function() {
        this.value = this.value.replace(/[^0-9]/g, ''); // Only digits are allowed
    });

    zipInput.addEventListener('blur', function() {
        validateZipcode(); // Validate when the field loses focus
    });
});

function validateZipcode() {
    const zipInput = document.getElementById('pincode');
    const zipError = document.getElementById('pincode_error');
    const zipcode = zipInput.value.trim();
    zipError.textContent = ''; // Clear previous error

    // Ensure the value is not empty
    if (zipcode.length === 0) {
        zipError.textContent = 'Zip code is required';
        return false;
    }

    // Ensure the zip code is exactly 6 digits
    if (zipcode.length !== 6) {
        zipError.textContent = 'Zip code must be exactly 6 digits';
        return false;
    }

    // Ensure the zip code contains only digits
    if (isNaN(zipcode)) {
        zipError.textContent = 'Zip code must contain only numbers';
        return false;
    }

    return true;
}



