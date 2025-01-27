//configure global variable
const config = {
    host: 'http://localhost:8000'
}

$('#logout').click(function () {
    swal({
            title: "ออกจากระบบ?",
            text: "คุณต้องการออกจากระบบใช่หรือไม่",
            icon: "warning",
            buttons: ["No", "Yes"],
            dangerMode: true
        })
        .then((event) => {
            if (event) {
                userLogOut();
            } else {}
        });
});



function getUrlVars() {
    var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
        vars[key] = value;
    });
    return vars;
}
function passportAuthenticate() {
    var auth = $.cookie().auth;
    if (auth) {

        auth = JSON.parse(auth);
        return auth;
    } else {
        return null;
    }
}

function setCookie(title, value) {
    $.cookie(title, value, {
        expires: 365
    });
}

function getCookie() {
    return $.cookie();
}

function removeCookieByTitle(title) {
    $.removeCookie(title);
}

function userLogOut() {
    var cookies = $.cookie();
    for (let cookie in cookies) {
        $.removeCookie(cookie);
    }
    location.href = 'login.html';
}

function callAPI(data, callback) {
  // console.log(data);
    $.ajax({
        url: data.url,
        data: data.data,
        type: data.type,
        dataType: 'json',
        crossDomain: true,
        success: function (data, textStatus, xhr) {
            return callback(data);
        },
        error: function (xhr, textStatus, errorThrown) {
          console.log(textStatus);
          console.log(errorThrown);
           return callback(textStatus);
            //swal('', xhr.responseJSON, errorThrown);
        }
    });
}


function validateEmail(email) {
    var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
}

function empty(mixed_var) {
    var undef, key, i, len
    var emptyValues = [undef, null, false, 0, '', '0']
    for (i = 0, len = emptyValues.length; i < len; i++) {
        if (mixed_var === emptyValues[i]) {
            return true
        }
    }
    if (typeof mixed_var === 'object') {
        for (key in mixed_var) {
            return false
        }
        return true
    }
    return false
}
