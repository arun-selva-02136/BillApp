// form validation
// Category name
function catname(inputField) {
  var regex = /^[A-Za-z]+$/;
  var inputValue = inputField.value;

  if (inputValue.length > 20) {
    inputField.value = inputValue.substring(0, 20);
  }

  if (!regex.test(inputValue)) {
    inputField.value = inputValue.replace(/[^A-Za-z]/g, "");
    document.getElementById("name_error").textContent =
      "Only A-Z and a-z are allowed with a max length of 20.";
  } else {
    document.getElementById("name_error").textContent = "";
  }
}

function code(inputField) {
  var regex = /^[A-Z0-9]+$/;
  var inputValue = inputField.value;

  if (inputValue.length > 6) {
    inputField.value = inputValue.substring(0, 6);
  }

  if (!regex.test(inputValue)) {
    inputField.value = inputValue.replace(/[^A-Z0-9]/g, "");
    document.getElementById("code_error").textContent =
      "Only A-Z and 0-9are allowed with a max length of 6.";
  } else {
    document.getElementById("code_error").textContent = "";
  }
}

function validateForm() {
  var CategoryNameInput = document.getElementById("categoryname");
  var CategoryCodeInput = document.getElementById("category_code");

  catname(CategoryNameInput);
  code(CategoryCodeInput);

  var CategoryNameError = document.getElementById("name_error").textContent;
  var CategoryCodeError = document.getElementById("code_error").textContent;

  if (CategoryNameError.trim() !== "" || CategoryCodeError.trim() !== "") {
    return false;
  }
  return true;
}
/// file input
function displayFileName() {
  var fileInput = document.getElementById("file-input");
  var fileName = fileInput.files[0].name;
  // Display the file name in another div
  var fileNameDisplay = document.getElementById("fileNameDisplay");
  fileNameDisplay.style.color = "green";
  fileNameDisplay.innerText = "Selected File: " + fileName;
}
