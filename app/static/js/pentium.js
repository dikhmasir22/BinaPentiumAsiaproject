function toggleside () {
  $('#sidebar').slideToggle()
  $('#main').toggleClass('toggleside')
}

function sign_in () {
  let email = $('#input-email').val()
  let password = $('#input-password').val()

  //  kondisi

  $.ajax({
    type: 'POST',
    url: '/login',
    data: {
      email: email,
      password: password
    },
    success: function (response) {
      if (response['result'] === 'success') {
        $.cookie('BinaAsiaDigitalindo', response['token'], { path: '/' });
        window.location.replace('/dashboard');
      } else {
        alert(response['msg'])
      }
    }
  })
}

function sign_out () {
  $.removeCookie('BinaAsiaDigitalindo', { path: '/' })
  alert('Kamu telah Logged Out!')
  window.location.href = '/'
}