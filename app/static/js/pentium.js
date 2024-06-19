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
        $.cookie('BinaAsiaDigitalindo', response['token'], { path: '/' })
        window.location.replace('/dashboard?msg=' + response['result'])
      } else {
        alert(response['msg'])
      }
    }
  })
}

function sign_out () {
  $.removeCookie('BinaAsiaDigitalindo', { path: '/' })
  Swal.fire({
    toast: true,
    position: 'top-end',
    icon: 'warning',
    title: 'Kamu Telah Logout!',
    showConfirmButton: false,
    timer: 1000,
    timerProgressBar: true,
    didOpen: toast => {
      toast.addEventListener('mouseenter', Swal.stopTimer)
      toast.addEventListener('mouseleave', Swal.resumeTimer)
    }
  })
  setTimeout(function () {
    window.location.href = '/'
  }, 1500)
}

function tampil_form () {
  $('#tambah_materi').addClass('d-none')
  $('#bungkus').removeClass('d-none')
  setTimeout(function () {
    $('#bungkus').addClass('tampil')
  }, 10)
  $('#input-materi').focus()
}

function batal () {
  $('#bungkus').removeClass('tampil')
  $('#bungkus').addClass('d-none')
  $('#tambah_materi').removeClass('d-none')
}

function link_youtube () {
  $('#bungkusan-link-yutub').removeClass('d-none')
  setTimeout(function () {
    $('#bungkusan-link-yutub').addClass('tampil')
  }, 10)
  $('#bungkusan-gambar').removeClass('tampil')
  $('#bungkusan-penjelasan').removeClass('tampil')
  setTimeout(function () {
    $('#bungkusan-gambar, #bungkusan-penjelasan').addClass('d-none')
  }, 500)
  $('#input-link-yutub').focus()
}

function gambar_tambah () {
  $('#bungkusan-link-yutub').removeClass('tampil')
  $('#bungkusan-gambar').removeClass('d-none')
  setTimeout(function () {
    $('#bungkusan-gambar').addClass('tampil')
  }, 10)
  $('#bungkusan-penjelasan').removeClass('tampil')
  setTimeout(function () {
    $('#bungkusan-link-yutub, #bungkusan-penjelasan').addClass('d-none')
  }, 500)
  $('#form-gambar-tambah').focus()
}

function penjelasan () {
  $('#bungkusan-link-yutub').removeClass('tampil')
  $('#bungkusan-gambar').removeClass('tampil')
  $('#bungkusan-penjelasan').removeClass('d-none')
  setTimeout(function () {
    $('#bungkusan-penjelasan').addClass('tampil')
  }, 10)
  setTimeout(function () {
    $('#bungkusan-link-yutub, #bungkusan-gambar').addClass('d-none')
  }, 500)
  $('#input-judul-penjelasan').focus()
  $('#textarea-penjelasan').focus()
}

function batalkan () {
  $(
    '#bungkusan-link-yutub, #bungkusan-gambar, #bungkusan-penjelasan'
  ).removeClass('tampil')
  setTimeout(function () {
    $(
      '#bungkusan-link-yutub, #bungkusan-gambar, #bungkusan-penjelasan'
    ).addClass('d-none')
  }, 500)
}

function previewImage (event) {
  let reader = new FileReader()
  reader.onload = function () {
    let img = document.getElementById('gambar-preview')
    img.src = reader.result
  }
  reader.readAsDataURL(event.target.files[0])
}