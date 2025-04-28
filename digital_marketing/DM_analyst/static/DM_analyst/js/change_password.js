function validatePassword() {
    var password = $('#new_password').val();
    var confirm_password = $('#confirm_password').val();
    var valid = true;

    $('#minChars').toggleClass('valid', password.length >= 8);
    $('#upperCase').toggleClass('valid', /[A-Z]/.test(password));
    $('#specialChar').toggleClass('valid', /[!@#$%^&*(),.?":{}|<>]/.test(password));
    $('#digit').toggleClass('valid', /\d/.test(password));
    $('#passwordMatch').toggleClass('valid', password === confirm_password);

    if (password.length < 8 || !/[A-Z]/.test(password) || !/\d/.test(password) || 
        !/[!@#$%^&*(),.?":{}|<>]/.test(password) || password !== confirm_password) {
        valid = false;
    }

    $('button[type="submit"]').prop('disabled', !valid);
}
