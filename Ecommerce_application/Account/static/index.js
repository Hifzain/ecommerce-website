document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('register_form');
    const inputs = form.querySelectorAll('input');

    // Add event listener to each input field for real-time validation
    inputs.forEach(input => {
        input.addEventListener('input', () => validateField(input));
    });

    form.addEventListener('submit', e => {
        e.preventDefault();
        validateForm();
    });

    const setError = (element, message) => {
        const inputControl = element.parentElement;
        const errorDisplay = inputControl.querySelector('.error');

        errorDisplay.innerText = message;
        inputControl.classList.add('error');
        inputControl.classList.remove('success');
    };

    const setSuccess = element => {
        const inputControl = element.parentElement;
        const errorDisplay = inputControl.querySelector('.error');

        errorDisplay.innerText = '';
        inputControl.classList.add('success');
        inputControl.classList.remove('error');
    };

    const validateField = (element) => {
        const value = element.value.trim();
        let isValid = false;

        switch (element.id) {
            case 'fname':
                isValid = value !== '';
                setValidationState(element, isValid, 'First name is required');
                break;
            case 'lname':
                isValid = value !== '';
                setValidationState(element, isValid, 'Last name is required');
                break;
            case 'email':
                isValid = validateEmail(value);
                setValidationState(element, isValid, 'Valid email is required');
                break;
            case 'password':
                isValid = value.length >= 6; // Example: Password must be at least 6 characters
                setValidationState(element, isValid, 'Password must be at least 6 characters');
                break;
            case 'password2':
                isValid = value === document.getElementById('password').value;
                setValidationState(element, isValid, 'Passwords must match');
                break;
            default:
                break;
        }
    };

    const setValidationState = (element, isValid, message) => {
        if (isValid) {
            setSuccess(element);
        } else {
            setError(element, message);
        }
    };

    const validateEmail = (email) => {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(String(email).toLowerCase());
    };

    const validateForm = () => {
        inputs.forEach(input => validateField(input));
        // Additional form submission logic can be added here
    };
});
