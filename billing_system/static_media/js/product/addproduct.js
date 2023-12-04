// form validation

const form = document.querySelector("#form");
const productName = document.querySelector("#productname");

const Quantity = document.querySelector("#Quantity");

const Tax = document.querySelector("#Tax");
const HSNCode = document.querySelector("#HSNCode");
const MRPPrice = document.querySelector("#MRPPrice");
const Price = document.querySelector("#Price");
const Category = document.querySelector("#Category");
const Brand = document.querySelector("#Brand");
const Unit = document.querySelector("#Unit");
const Status = document.querySelector("#Status");
const select = document.querySelectorAll("select");

form.addEventListener("submit", (e) => {
  e.preventDefault();
  validateInputs();
  validateSelects();
});
function validateSelects() {}
function validateInputs() {
  const productNameVal = productName.value.trim();

  const QuantityVal = Quantity.value.trim();

  const TaxVal = Tax.value.trim();
  const HSNCodeVal = HSNCode.value.trim();
  const MRPPriceVal = MRPPrice.value.trim();
  const PriceVal = Price.value.trim();
  const CategoryVal = Category.value.trim();
  const BrandVal = Brand.value.trim();
  const StatusVal = Status.value.trim();
  const UnitVal = Unit.value.trim();

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

  if (QuantityVal === "") {
    setError(Quantity, "field  should not empty");
    allConditionsTrue = false;
  } else {
    setSuccess(Quantity);
  }

  if (TaxVal === "") {
    setError(Tax, "field  should not empty");
    allConditionsTrue = false;
  } else if (validatePercent(TaxVal) && TaxVal.slice(-1) === "%") {
    setError(Tax, "enter symbol % ");

    allConditionsTrue = false;
  } else {
    setSuccess(Tax);
  }
  if (HSNCodeVal === "") {
    setError(HSNCode, "field  should not empty");
    allConditionsTrue = false;
  } else {
    setSuccess(HSNCode);
  }
  if (MRPPriceVal === "") {
    setError(MRPPrice, "field  should not empty");
    allConditionsTrue = false;
  } else if (validateNumber(MRPPriceVal)) {
    setError(MRPPrice, "pls enternumber");
    allConditionsTrue = false;
  } else {
    setSuccess(MRPPrice);
  }
  if (PriceVal === "") {
    setError(Price, "field  should not empty");
    allConditionsTrue = false;
  } else if (validateNumber(PriceVal)) {
    setError(Price, "pls enternumber");
    allConditionsTrue = false;
  } else {
    setSuccess(Price);
  }
  if (CategoryVal === "") {
    setError(Category, "field  should not empty");
    allConditionsTrue = false;
  } else {
    setSuccess(Category);
  }
  if (BrandVal === "") {
    setError(Brand, "field  should not empty");
    allConditionsTrue = false;
  } else {
    setSuccess(Brand);
  }
  if (UnitVal === "") {
    setError(Unit, "field  should not empty");
    allConditionsTrue = false;
  } else {
    setSuccess(Unit);
  }
  if (StatusVal === "") {
    setError(Status, "field  should not empty");
    allConditionsTrue = false;
  } else {
    setSuccess(Status);
  }

  //   var selects = document.querySelectorAll("select");
  //   var results = [];
  //   for (var i = 0; i < selects.length; i++) {
  //     var selectedValue = selects[i].value;

  //     if (selectedValue !== "") {
  //       results.push(selectedValue);
  //       var id = selects[i].id;
  //       var selectedid = document.querySelectorAll(`id}`);
  //       console.log(selectedid.value);

  //       // If any select has a value, set 'a' to false and break out of the loop
  //     } else {
  //       setError();
  //     }
  //   }

  //   if (results.length === selects.length) {
  //     alert("All  selected.");
  //     console.log(results);
  //   } else {
  //     allConditionsTrue = false;
  //     alert("At least one select tag has a value selected.");
  //   }

  if (allConditionsTrue) {
    form.submit();
  }
}

function setError(element, message) {
  const inputGroup = element.parentElement;
  const errorElement = inputGroup.querySelector(".error");

  //   var formselect = document.getElementsByClassName("form-select");
  //   var formcontrol = document.getElementsByClassName("form-control");
  //   for (i = 0; i < formselect.length; i++) {
  //     formselect[i].style.border = "1px solid red";
  //   }
  //   for (i = 0; i < formcontrol.length; i++) {
  //     formcontrol[i].style.border = "1px solid red";
  //   }
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
