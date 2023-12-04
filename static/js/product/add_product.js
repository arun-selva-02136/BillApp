// PRODUCT NAME

function validateProductName(inputField) {
  var regex = /^[A-Za-z0-9\-_]+$/;
  var inputValue = inputField.value;

  if (!regex.test(inputValue)) {
    inputField.value = inputValue.replace(/[^A-Za-z0-9\-_]/g, "");
    document.getElementById("product_name_error").textContent =
      'Only A-Z, a-z, 0-9, "-", and "_" are allowed.';
  } else {
    document.getElementById("product_name_error").textContent = "";
  }
}

// CATEGORY

function category(selectElement) {
  var selectedValue = selectElement.value;
  // var categoryError = document.getElementById('category_error');

  if (selectedValue === "") {
    document.getElementById("category_error").textContent =
      "Please select a category.";
  } else {
    document.getElementById("category_error").textContent = "";
  }
}

// SUB CATEGORY

function subCategory(inputField) {
  var regex = /^[A-Za-z0-9\-_]+$/;
  var inputValue = inputField.value;

  if (!regex.test(inputValue)) {
    inputField.value = inputValue.replace(/[^A-Za-z0-9\-_]/g, "");
    document.getElementById("sub_category_error").textContent =
      'Only A-Z, a-z, 0-9, "-", and "_" are allowed.';
  } else {
    document.getElementById("sub_category_error").textContent = "";
  }
}

// BRAND

function ProdBrand(inputField) {
  var regex = /^[A-Za-z0-9\-_]+$/;
  var inputValue = inputField.value;

  if (!regex.test(inputValue)) {
    inputField.value = inputValue.replace(/[^A-Za-z0-9\-_]/g, "");
    document.getElementById("brand_error").textContent =
      'Only A-Z, a-z, 0-9, "-", and "_" are allowed.';
  } else {
    document.getElementById("brand_error").textContent = "";
  }
}

// UNIT

function unit(inputField) {
  var regex = /^[A-Za-z]+$/;
  var inputValue = inputField.value;

  if (inputValue.length > 6) {
    inputField.value = inputValue.substring(0, 6);
  }

  if (!regex.test(inputValue)) {
    inputField.value = inputValue.replace(/[^A-Za-z]/g, "");
    document.getElementById("unit_error").textContent =
      "Only A-Z and a-z are allowed.";
  } else {
    document.getElementById("unit_error").textContent = "";
  }
}

// SKU (IT'S NOT A FORM VALIDATION)

function Productsku() {
  var inputField = document.getElementById("SKU");
  var regex = /^[A-Z0-9]+$/;
  var inputValue = inputField.value;

  if (inputValue.length > 8) {
    inputField.value = inputValue.substring(0, 8);
  }

  if (!regex.test(inputField.value)) {
    inputField.value = inputValue.replace(/[^A-Z0-9]/g, "");
    document.getElementById("sku_error").textContent =
      "Only A-Z and 0-9 are allowed with a maximum length of 8.";
  } else {
    document.getElementById("sku_error").textContent = "";
  }
}

// VENDOR

function vendor(selectvendor) {
  var vendorValue = selectvendor.value;
  // var categoryError = document.getElementById('category_error');

  if (vendorValue === "") {
    document.getElementById("vendor_error").textContent =
      "Please select a Vendor ID.";
  } else {
    document.getElementById("vendor_error").textContent = "";
  }
}

// QUANTITY

function qty(inputField) {
  var inputValue = inputField.value;

  if (inputValue === "." && inputValue.length >= 7) {
    inputField.value = inputValue.substring(0, 7);
  }

  if (inputValue !== "." && inputValue.length >= 7) {
    inputField.value = inputValue.substring(0, 7);
  }

  var regex = /^[0-9.]+$/;

  // Check for leading period
  if (inputValue.indexOf(".") === 0) {
    inputField.value = inputValue.substring(1);
  }

  // Check for multiple periods
  if ((inputValue.match(/\./g) || []).length > 1) {
    inputField.value = inputValue.substring(0, inputValue.lastIndexOf("."));
  }

  if (!regex.test(inputField.value)) {
    inputField.value = inputValue.replace(/[^0-9.]/g, "");
    document.getElementById("qty_error").textContent =
      'Only 0-9 and "." are allowed with a max length of 7, and only one period is allowed.';
  } else {
    document.getElementById("qty_error").textContent = "";
  }
}

// GST

function tax(inputField) {
  var inputValue = inputField.value;

  // Check for dot and set maxLength accordingly
  if (inputValue.includes(".")) {
    inputField.maxLength = 5; // 5 digits + 1 dot
  } else if (inputValue.length >= 3) {
    inputField.maxLength = 3;
  }

  // Allow only 0-9, '.', and '%'
  var regex = /^[0-9.%]+$/;
  if (!regex.test(inputField.value)) {
    inputField.value = inputValue.replace(/[^0-9.%]/g, "");
    document.getElementById("tax_error").textContent =
      'Only 0-9, ".", and "%" are allowed.';
  }
  // Check if the input ends with '%', if not, add it
  else if (!inputValue.endsWith("%")) {
    document.getElementById("tax_error").textContent =
      "it is valide end with %";
    // inputField.value = inputValue + '%';
  } else {
    document.getElementById("tax_error").textContent = "";
  }
}

// DISCOUNT (IT'S NOT A FORM VALIDATION)

function prodiscount(inputField) {
  inputField = document.getElementById("Discount");
  var inputValue = inputField.value;

  // Check for dot and set maxLength accordingly
  if (inputValue.includes(".")) {
    inputField.maxLength = 5; // 5 digits + 1 dot
  } else if (inputValue.length >= 3) {
    inputField.maxLength = 3;
  }

  // Allow only 0-9, '.', and '%'
  var regex = /^[0-9.%]+$/;
  if (!regex.test(inputField.value)) {
    inputField.value = inputValue.replace(/[^0-9.%]/g, "");
    document.getElementById("discount_error").textContent =
      'Only 0-9, ".", and "%" are allowed.';
  } else if (!inputValue.endsWith("%")) {
    document.getElementById("discount_error").textContent =
      "it is valide end with %";
    // inputField.value = inputValue + '%';
  } else {
    // Check if the input ends with '%', if not, add it
    document.getElementById("discount_error").textContent = "";
  }
}

// HSN

function hsn(inputField) {
  var regex = /^[0-9]+$/;
  var inputValue = inputField.value;

  if (inputValue.length > 8) {
    inputField.value = inputValue.substring(0, 8);
  }

  if (!regex.test(inputField.value)) {
    inputField.value = inputValue.replace(/[^0-9]/g, "");
    document.getElementById("hsn_error").textContent =
      "Only 0-9 are allowed with a max length of 8.";
  } else {
    document.getElementById("hsn_error").textContent = "";
  }
}

// MRP

function promrp(inputField) {
  var inputValue = inputField.value;

  if (inputValue === "." && inputValue.length >= 7) {
    inputField.value = inputValue.substring(0, 7);
  }

  if (inputValue !== "." && inputValue.length >= 7) {
    inputField.value = inputValue.substring(0, 7);
  }

  var regex = /^[0-9.]+$/;

  // Check for leading period
  if (inputValue.indexOf(".") === 0) {
    inputField.value = inputValue.substring(1);
  }

  // Check for multiple periods
  if ((inputValue.match(/\./g) || []).length > 1) {
    inputField.value = inputValue.substring(0, inputValue.lastIndexOf("."));
  }

  if (!regex.test(inputField.value)) {
    inputField.value = inputValue.replace(/[^0-9.]/g, "");
    document.getElementById("mrp_error").textContent =
      'Only 0-9 and "." are allowed with a max length of 7, and only one period is allowed.';
  } else {
    document.getElementById("mrp_error").textContent = "";
  }
}

// PRICE

function proprice(inputField) {
  var inputValue = inputField.value;

  if (inputValue === "." && inputValue.length >= 7) {
    inputField.value = inputValue.substring(0, 7);
  }

  if (inputValue !== "." && inputValue.length >= 7) {
    inputField.value = inputValue.substring(0, 7);
  }

  var regex = /^[0-9.]+$/;

  // Check for leading period
  if (inputValue.indexOf(".") === 0) {
    inputField.value = inputValue.substring(1);
  }

  // Check for multiple periods
  if ((inputValue.match(/\./g) || []).length > 1) {
    inputField.value = inputValue.substring(0, inputValue.lastIndexOf("."));
  }

  if (!regex.test(inputField.value)) {
    inputField.value = inputValue.replace(/[^0-9.]/g, "");
    document.getElementById("price_error").textContent =
      'Only 0-9 and "." are allowed with a max length of 7, and only one period is allowed.';
  } else {
    document.getElementById("price_error").textContent = "";
  }
}

// STATUS

function status(selectStatus) {
  var statusValue = selectStatus.value;
  // var categoryError = document.getElementById('category_error');

  if (statusValue === "") {
    document.getElementById("status_error").textContent =
      "Please select a status.";
  } else {
    document.getElementById("status_error").textContent = "";
  }
  // var regex = /^\s*$/;

  // if (regex.test(statusValue)) {
  //   selectStatus.value = statusValue.replace(/[^\s]/g, '');
  //   document.getElementById('status_error').textContent = 'Please enter a non-empty value.';
  // } else {
  //   document.getElementById('status_error').textContent = '';
  // }
}

// BUTTON
// SKU AND DISCOUNT NOT EXCEPTED HERE REASON OF THAT TWO FIELD HAVE (ONKEYUP) VALIDATION ONLY
function validateForm() {
  var productNameInput = document.getElementById("product_name");
  var categoryval = document.getElementById("Category");
  // var subcategory = document.getElementById('sub_category');
  var brandname = document.getElementById("Brand");
  var unitname = document.getElementById("Unit");
  var vendorval = document.getElementById("Vendor");
  var quantity = document.getElementById("Quantity");
  var Taxval = document.getElementById("Tax");
  var hsnval = document.getElementById("HSNCode");
  var mrpval = document.getElementById("MRPPrice");
  var priceval = document.getElementById("Price");
  var statusval = document.getElementById("Status");

  validateProductName(productNameInput);
  category(categoryval);
  // subCategory(subcategory)
  ProdBrand(brandname);
  unit(unitname);
  vendor(vendorval);
  qty(quantity);
  tax(Taxval);
  hsn(hsnval);
  promrp(mrpval);
  proprice(priceval);
  status(statusval);

  var productNameError =
    document.getElementById("product_name_error").textContent;
  var categoryError = document.getElementById("category_error").textContent;
  // var SubCategoryError = document.getElementById('sub_category_error').textContent;
  var BrandError = document.getElementById("brand_error").textContent;
  var UnitError = document.getElementById("unit_error").textContent;
  var vendorError = document.getElementById("vendor_error").textContent;
  var qtyError = document.getElementById("qty_error").textContent;
  var taxError = document.getElementById("tax_error").textContent;
  var hsnError = document.getElementById("hsn_error").textContent;
  var mrpError = document.getElementById("mrp_error").textContent;
  var priceError = document.getElementById("price_error").textContent;
  var statusError = document.getElementById("status_error").textContent;

  if (
    productNameError.trim() !== "" ||
    categoryError.trim() !== "" ||
    BrandError.trim() !== "" ||
    UnitError.trim() !== "" ||
    vendorError.trim() !== "" ||
    qtyError.trim() !== "" ||
    taxError.trim() !== "" ||
    hsnError.trim() !== "" ||
    mrpError.trim() !== "" ||
    priceError.trim() !== "" ||
    statusError.trim() !== ""
  ) {
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