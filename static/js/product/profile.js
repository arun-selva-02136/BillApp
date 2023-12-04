// Example starter JavaScript for disabling form submissions if there are invalid fields
(() => {
  'use strict'

  // Fetch all the forms we want to apply custom Bootstrap validation styles to
  const forms = document.querySelectorAll('.needs-validation')

  // Loop over them and prevent submission
  Array.from(forms).forEach(form => {
    form.addEventListener('submit', event => {
      if (!form.checkValidity()) {
        event.preventDefault()
        event.stopPropagation()
      }

      form.classList.add('was-validated')
    }, false)
  })
})()


const proImg = document.querySelector('#Profole-image');
const photo = document.querySelector('#photo');
const file = document.querySelector('#file');
const uploadBtn = document.querySelector('#uploadBtn');




file.addEventListener('change', function () {
  const chosedFile = this.files[0];
  if (chosedFile) {
    const reader = new FileReader();
    reader.addEventListener('load', function () {
      photo.setAttribute('src', reader.result)
    })
    reader.readAsDataURL(chosedFile)
  }
})

var logoHeader = document.querySelector('#logo-header');
var logo = document.querySelector('#logo');
var edit = document.querySelector('#edit');
var logoEdit = document.querySelector('#logo-edit');

edit.addEventListener('change', function () {
  const chosedFile1 = this.files[0];
  if (chosedFile1) {
    const reader1 = new FileReader();
    reader1.addEventListener('load', function () {
      logo.setAttribute('src', reader1.result)
    })
    reader1.readAsDataURL(chosedFile1)
  }
})



// Profile Header Banner color Change
const colorPickerIcon = document.getElementById('colorPickerIcon');
const ProfileIcon = document.getElementById('Profile-icon');
const colorPicker = document.getElementById('colorPicker');
const LogoHeader = document.getElementById('logoHeader');

colorPickerIcon.addEventListener('click', () => {
  colorPicker.click();
});

colorPicker.addEventListener('input', () => {
  const selectedColor = colorPicker.value;
  LogoHeader.style.backgroundColor = selectedColor;
  colorPickerIcon.style.color = 'black'
  ProfileIcon.style.color = 'black'
});
// Profile Header Banner color Change