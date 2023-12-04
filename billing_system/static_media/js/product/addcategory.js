// form validation

const form = document.querySelector("#form");
const productName = document.querySelector("#productname");
const Category = document.querySelector("#Category");
const select = document.querySelectorAll("select");
form.addEventListener("submit", (e) => {
  e.preventDefault();
  validateInputs();
  validateSelects();
});
function validateSelects() {}
function validateInputs() {
  const productNameVal = productName.value.trim();
  const CategoryVal = Category.value.trim();

  allConditionsTrue = true;

  if (productNameVal === "") {
    setError(productName, "field  should not empty");
    allConditionsTrue = false;
  } else if (validatetext(productNameVal)) {
    setError(productName, "First Start with Number");
    allConditionsTrue = false;
  } else {
    setSuccess(productName);
  }
  if (CategoryVal === "") {
    setError(Category, "field  should not empty");
    allConditionsTrue = false;
  } else {
    setSuccess(Category);
  }

  if (allConditionsTrue) {
    form.submit();
  }
}

function setError(element, message) {
  const inputGroup = element.parentElement;
  const errorElement = inputGroup.querySelector(".error");
  errorElement.innerText = message;
  inputGroup.classList.add("error");
  inputGroup.classList.remove("success");
}

function setSuccess(element) {
  const inputGroup = element.parentElement;
  const errorElement = inputGroup.querySelector(".error");

  errorElement.innerText = "";
  inputGroup.classList.add("success");
  inputGroup.classList.remove("error");
}

const FirstLetter = /^[ a-z]/;

const validateNumber = (text) => {
  return (
    String(text)
      // .toLowerCase()
      .match(/[ `!@#$%^&*()+\-=\[\]{};':"\\|,<>\/?~a-zA-Z]/)
  );
};
const validatePercent = (text) => {
  return (
    String(text)
      // .toLowerCase()
      .match(/[ `!@#$^&*()+\-=\[\]{};'.:"\\|,<>\/?~a-zA-Z]/)
  );
};
const validatetext = (text) => {
  return (
    String(text)
      // .toLowerCase()
      .match(/[ `!@#$%^&*()+\=\[\]{};':"\\|,.<>\/?~]/)
  );
};
