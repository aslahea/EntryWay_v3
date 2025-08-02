

// ------------------ Shared Error Handlers ------------------
function showError(input, message) {
    const errorDiv = input.closest('.mb-3')?.querySelector('.error-message') ||
        input.closest('.form-check')?.querySelector('.error-message');
    input.classList.add('is-invalid');
    if (errorDiv) errorDiv.textContent = message;
}

function clearError(input) {
    input.classList.remove('is-invalid');
    const errorDiv = input.closest('.mb-3')?.querySelector('.error-message') ||
        input.closest('.form-check')?.querySelector('.error-message');
    if (errorDiv) errorDiv.textContent = '';
}



// ------------------ Registration Field Validators ------------------
function validateUsername(input) {
    const usernameRegex = /^[a-zA-Z0-9_]{3,20}$/;
    if (!input.value.trim()) {
        showError(input, 'Username is required.');
        return false;
    } else if (!usernameRegex.test(input.value)) {
        showError(input, 'Username must be 3-20 characters and contain only letters, numbers, or underscores.');
        return false;
    }
    clearError(input);
    return true;
}

function validateEmail(input) {
    const value = input.value.trim();
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!regex.test(value)) {
        showError(input, 'Enter a valid email.');
        return false;
    }
    clearError(input);
    return true;
}

function validatePassword(input) {
    const value = input.value.trim();
    if (value.length < 8) {
        showError(input, 'Password must be at least 8 characters.');
        return false;
    }
    clearError(input);
    return true;
}

function validateConfirmPassword(passwordInput, confirmInput) {
    if (passwordInput.value !== confirmInput.value) {
        showError(confirmInput, 'Passwords do not match.');
        return false;
    }
    clearError(confirmInput);
    return true;
}

function validateDOB(input) {
    if (!input.value) {
        showError(input, 'Please select your date of birth.');
        return false;
    }
    clearError(input);
    return true;
}

function validateGender(input) {
    if (!input.value) {
        showError(input, 'Please select a gender.');
        return false;
    }
    clearError(input);
    return true;
}

function validateMaritalStatus() {
    const radios = document.getElementsByName('marital_status');
    let selected = false;
    const container = radios[0]?.closest('.mb-3');
    const errorDiv = container?.querySelector('.error-message');
    for (let i = 0; i < radios.length; i++) {
        if (radios[i].checked) {
            selected = true;
            break;
        }
    }
    if (!selected) {
        if (errorDiv) errorDiv.textContent = 'Select marital status';
        return false;
    }
    if (errorDiv) errorDiv.textContent = '';
    return true;
}

function validateTerms(input) {
    const errorDiv = input.closest('.form-check')?.querySelector('.error-message');
    if (!input.checked) {
        if (errorDiv) errorDiv.textContent = 'You must agree to the terms';
        input.classList.add('is-invalid');
        return false;
    }
    if (errorDiv) errorDiv.textContent = '';
    input.classList.remove('is-invalid');
    return true;
}





// ------------------ Registration Form Validation ------------------
function attachFormValidation(formId) {
    const form = document.getElementById(formId);
    const submitBtn = document.getElementById("submitBtn");
    const username = document.getElementById("username");
    const email = document.getElementById("email");
    const password1 = document.getElementById("password1");
    const password2 = document.getElementById("password2");
    const dob = document.getElementById("dob");
    const gender = document.getElementById("gender");
    const terms = document.getElementById("terms");
    const maritalRadios = document.getElementsByName("marital_status");

    function validateAllFields() {
        const isValid =
            validateUsername(username) &&
            validateEmail(email) &&
            validatePassword(password1) &&
            validateConfirmPassword(password1, password2) &&
            validateDOB(dob) &&
            validateGender(gender) &&
            validateMaritalStatus() &&
            validateTerms(terms);

        submitBtn.disabled = !isValid;
        submitBtn.classList.toggle('disabled', !isValid);
    }

    [username, email, password1, password2, dob, gender, terms].forEach(input => {
        input.addEventListener("input", validateAllFields);
        input.addEventListener("blur", validateAllFields);
        input.addEventListener("change", validateAllFields);
    });

    for (let i = 0; i < maritalRadios.length; i++) {
        maritalRadios[i].addEventListener("change", validateAllFields);
    }

    form.addEventListener("submit", function (e) {
        validateAllFields();
        if (submitBtn.disabled) {
            e.preventDefault();
        }
    });

    validateAllFields();
}




// ------------------ Login Form Validation ------------------
function attachLoginValidation(formId) {
    const form = document.getElementById(formId);
    const submitBtn = document.getElementById("loginBtn");
    const username = document.getElementById("username");
    const password = document.getElementById("password");

    function validateLoginFields() {
        let isValid = true;

        // Username check
        if (!username.value.trim()) {
            showError(username, "Username is required.");
            isValid = false;
        } else {
            clearError(username);
        }

        // Password check
        if (!password.value.trim()) {
            showError(password, "Password is required.");
            isValid = false;
        } else {
            clearError(password);
        }

        submitBtn.disabled = !isValid;
        submitBtn.classList.toggle('disabled', !isValid);
    }

    [username, password].forEach(input => {
        input.addEventListener("input", validateLoginFields);
        input.addEventListener("blur", validateLoginFields);
    });

    form.addEventListener("submit", function (e) {
        validateLoginFields();
        if (submitBtn.disabled) {
            e.preventDefault();
        }
    });

    validateLoginFields();
}


// ------------------ Admin Login Validation ------------------
function attachAdminLoginValidation(formId) {
    const form = document.getElementById(formId);
    const username = document.getElementById("adminUsername");
    const password = document.getElementById("adminPassword");
    const submitBtn = document.getElementById("adminLoginBtn");

    function validateFields() {
        let isValid = true;

        if (!username.value.trim()) {
            showError(username, "Username is required.");
            isValid = false;
        } else {
            clearError(username);
        }

        if (!password.value.trim()) {
            showError(password, "Password is required.");
            isValid = false;
        } else {
            clearError(password);
        }

        submitBtn.disabled = !isValid;
        submitBtn.classList.toggle('disabled', !isValid);
    }

    [username, password].forEach(input => {
        input.addEventListener("input", validateFields);
        input.addEventListener("blur", validateFields);
    });

    form.addEventListener("submit", function (e) {
        validateFields();
        if (submitBtn.disabled) {
            e.preventDefault();
        }
    });

    validateFields();
}


// ------------------ Admin Create/Edit User Validation ------------------
function attachAdminUserFormValidation(formId, includePassword = false, includeTerms = false) {
    const form = document.getElementById(formId);
    const submitBtn = document.getElementById("adminSubmitBtn");

    const username = document.getElementById("username");
    const email = document.getElementById("email");
    const dob = document.getElementById("dob");
    const gender = document.getElementById("gender");
    const maritalRadios = document.getElementsByName("marital_status");

    const password1 = document.getElementById("password1");
    const password2 = document.getElementById("password2");
    const terms = document.getElementById("terms");

    function validateFields() {
        let isValid =
            validateUsername(username) &&
            validateEmail(email) &&
            validateDOB(dob) &&
            validateGender(gender) &&
            validateMaritalStatus();

        if (includePassword) {
            isValid = isValid &&
                validatePassword(password1) &&
                validateConfirmPassword(password1, password2);
        }

        if (includeTerms) {
            isValid = isValid && validateTerms(terms);
        }

        submitBtn.disabled = !isValid;
        submitBtn.classList.toggle('disabled', !isValid);
    }

    // Bind input/blur/change events
    [username, email, dob, gender].forEach(input => {
        input.addEventListener("input", validateFields);
        input.addEventListener("blur", validateFields);
        input.addEventListener("change", validateFields);
    });

    if (includePassword) {
        [password1, password2].forEach(input => {
            input.addEventListener("input", validateFields);
            input.addEventListener("blur", validateFields);
        });
    }

    if (includeTerms && terms) {
        terms.addEventListener("change", validateFields);
    }

    for (let i = 0; i < maritalRadios.length; i++) {
        maritalRadios[i].addEventListener("change", validateFields);
    }

    form.addEventListener("submit", function (e) {
        validateFields();
        if (submitBtn.disabled) {
            e.preventDefault();
        }
    });

    validateFields();
}
