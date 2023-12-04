function calculateRow(input) {
  var row = input.closest('tr');
  var productName = row.querySelector('td:nth-child(2) input').value.trim();
  var qty = parseFloat(row.querySelector('td:nth-child(4) input').value) || 0;
  var hnsCode = parseFloat(row.querySelector('td:nth-child(3) input').value) || 0;
  var sgstNo = parseFloat(row.querySelector('td:nth-child(5) input').value) || 0;
  var cgstNo = parseFloat(row.querySelector('td:nth-child(6) input').value) || 0;
  var amount = parseFloat(row.querySelector('td:nth-child(7) input').value) || 0;
  var discountAmount = parseFloat(row.querySelector('td:nth-child(8) input').value) || 0;
  var Empty = (amount * cgstNo /100)
  var diScount = (amount * discountAmount /100)
  var netAmount = (Empty + amount - diScount) * qty;


  row.querySelector('td:nth-child(9) span.net-amount').textContent = netAmount.toFixed(2);

  // Update HNS code, SGST No, CGST No totals
  // var hnsCodeTotal = calculateColumnTotal(3);
  var qtyTotal = calculateColumnTotal(4);
  var sgstNoTotal = calculateColumnTotal(5);
  var cgstNoTotal = calculateColumnTotal(6);

  // Calculate totals for all rows
  var totalNetAmount = 0;
  var totalQty = 0;
  var totalSgstNo = 0;
  var totalCgstNo = 0;
  var totalGstAmount = 0;
  var totalDiscountAmount = 0;

  // Iterate through all rows
  document.querySelectorAll('.product-row').forEach(function (row) {
    var currentQty = parseFloat(row.querySelector('td:nth-child(4) input').value) || 0;
    var currentHnsCode = parseFloat(row.querySelector('td:nth-child(3) input').value) || 0;
    var currentSgstNo = parseFloat(row.querySelector('td:nth-child(5) input').value) || 0;
    var currentCgstNo = parseFloat(row.querySelector('td:nth-child(6) input').value) || 0;
    var currentAmount = parseFloat(row.querySelector('td:nth-child(7) input').value) || 0;
    var currentDiscountAmount = parseFloat(row.querySelector('td:nth-child(8) input').value) || 0;

    totalQty += currentQty;
    totalSgstNo += currentSgstNo;
    totalCgstNo += currentCgstNo;

    var currentEmpty = (currentAmount * currentCgstNo / 100);
    var currentDiscount = (currentAmount * currentDiscountAmount / 100);
    var currentNetAmount = (currentEmpty + currentAmount - currentDiscount) * currentQty;

    totalNetAmount += currentNetAmount;
    totalGstAmount += currentEmpty;
    totalDiscountAmount += currentDiscount;
  });

  // document.getElementById('hns-code-total').textContent = hnsCodeTotal.toFixed(2);
  document.getElementById('qty-total').textContent = qtyTotal.toFixed();
  document.querySelector('.sgst-no-total').textContent = `${sgstNoTotal.toFixed('')}%`;
  document.querySelector('.cgst-no-total').textContent = `${cgstNoTotal.toFixed('')}%`;

  document.getElementById('SGST').textContent = `${sgstNoTotal.toFixed('')}%`;
  document.getElementById('Cgst').textContent = `${cgstNoTotal.toFixed('')}%`;
  document.getElementById('gstAmount').textContent = totalGstAmount.toFixed(1);
  document.getElementById('DiscountAmount').textContent = totalDiscountAmount.toFixed(1);

  // Add a new row if the last row is filled
 // Add a new row if the last row is filled based on qty
if (qty > 0 && input === row.querySelector('td:nth-child(4) input')) {
  var tableBody = document.getElementById('table-body');
  var lastRow = tableBody.lastElementChild;
  var qtyInput = lastRow.querySelector('td:nth-child(4) input');
  
  if (qtyInput.value.trim() !== "") {
    var newRow = document.createElement('tr');
    newRow.classList.add('product-row');
    newRow.innerHTML = row.innerHTML;
    var span = newRow.querySelector('.sno');
    span.textContent = tableBody.childElementCount + 1;

    newRow.querySelectorAll('input').forEach(function (input) {
      input.value = '';
    });

    newRow.querySelectorAll('.net-amount').forEach(function (span) {
      span.textContent = '0.00';
    });

    tableBody.appendChild(newRow);
  }
}


  // Update totals
  calculateTotals();
}

function calculateColumnTotal(columnIndex) {
  var rows = document.querySelectorAll('#product-table tbody tr.product-row');
  var total = 0;

  rows.forEach(function (row) {
    var value = parseFloat(row.querySelector('td:nth-child(' + columnIndex + ') input').value) || 0;
    total += value;
  });

  return total;
}

function calculateTotals() {
  var rows = document.querySelectorAll('#product-table tbody tr.product-row');
  var productListLength = 0;
  var totalAmount = 0;
  var totalDiscountAmount = 0;
  var totalNetAmount = 0;

  rows.forEach(function (row) {
    var productName = row.querySelector('td:nth-child(2) input').value.trim();
    if (productName !== "") {
      productListLength++;
    }

    var qty = parseFloat(row.querySelector('td:nth-child(4) input').value) || 0;
    var sgstNo = parseFloat(row.querySelector('td:nth-child(5) input').value) || 0;
    var cgstNo = parseFloat(row.querySelector('td:nth-child(6) input').value) || 0;
    var amount = parseFloat(row.querySelector('td:nth-child(7) input').value) || 0;
    var discountAmount = parseFloat(row.querySelector('td:nth-child(8) input').value) || 0;
    var enteredAmount = parseFloat(document.getElementById('amount-input').value) || 0;
    var empty = amount * cgstNo /100
    var DiScount = amount * discountAmount /100
    var netAmount = (empty + amount - DiScount) * qty;
    var balance = enteredAmount -  totalNetAmount.toFixed(2);

    totalAmount += amount;
    totalDiscountAmount += discountAmount;
    totalNetAmount += netAmount;
    document.getElementById('balance').textContent = balance.toFixed(2);
  });

  document.getElementById('product-list-length').textContent = productListLength;
  document.getElementById('total-amount').textContent = totalAmount.toFixed(2);
  document.getElementById('total-discount-amount').textContent = `${totalDiscountAmount.toFixed()}%`;
  document.getElementById('total-net-amount').textContent = totalNetAmount.toFixed(2);
  // document.getElementById('overall-total').textContent = totalNetAmount.toFixed(2);

  document.getElementById('discount').textContent = `${totalDiscountAmount.toFixed()}%`;
  document.getElementById('total').textContent = totalNetAmount.toFixed(2);
}




// Form Validation
// Example starter JavaScript for disabling form submissions if there are invalid fields
(function () {
  'use strict'

  // Fetch all the forms we want to apply custom Bootstrap validation styles to
  var forms = document.querySelectorAll('.needs-validation')

  // Loop over them and prevent submission
  Array.prototype.slice.call(forms)
    .forEach(function (form) {
      form.addEventListener('submit', function (event) {
        if (!form.checkValidity()) {
          event.preventDefault()
          event.stopPropagation()
        }

        form.classList.add('was-validated')
      }, false)
    })
})()
// Form Validation


// Popup show
// Popup show
// const productNameInput = productName;
// const sgstNoInput = sgstNo;
// const amountInput = document.getElementById('amount');
// const productNamePopup = document.getElementById('productNamePopup');
// const productNameList = document.getElementById('productNameList');

const tableBody = document.getElementById('table-body');
const productNamePopup = document.getElementById('productNamePopup');
const productNameList = document.getElementById('productNameList');

// const productInfo = [
//   { name: 'Apple', hns : '123355', qty : 1 , sgstNo: '5%', cgst : '3%' ,  amount: '10' ,discount : '1%' },
//   { name: 'Bat', hns : '123352', qty : 1 , sgstNo: '3%', cgst : '5%' ,  amount: '20' ,discount : '1%' },
//   { name: 'Cat', hns : '123353', qty : 1 , sgstNo: '2%', cgst : '3%' ,  amount: '30' ,discount : '1%' },
//   // Add more products as needed
// ];

function showSuggestions(input) {
  return function () {
    const inputText = input.value.trim().toLowerCase();

    if (inputText.length === 0) {
      productNamePopup.style.display = 'none';
      return;
    }

    const suggestions = productInfo.filter(product => product.name.toLowerCase().includes(inputText));

    productNameList.innerHTML = '';
    suggestions.forEach(product => {
      const listItem = document.createElement('li');
      // Display product name, sgstNo, and amount in the suggestion
      listItem.innerHTML = `<span>Product Name : ${product.name}</span> - <span>SGST NO :${product.sgstNo}</span> - <span>Price : ${product.amount}</span>`;
      listItem.onclick = () => fillProductName(input, product);
      productNameList.appendChild(listItem);
    });

    productNamePopup.style.display = suggestions.length > 0 ? 'block' : 'none';
  };
}

function fillProductName(input, product) {
  const row = input.closest('tr');
  row.querySelector('.product-name-input').value = product.name;
  row.querySelector('.sgst-no-input').value = product.sgstNo;
  row.querySelector('.amount-input').value = product.amount;
  row.querySelector('.HSN').value = product.hns;
  row.querySelector('.qty-input').value = product.qty;
  row.querySelector('.CGST').value = product.cgst;
  row.querySelector('.discount-amount-input').value = product.discount;
  row.querySelector('.pro_id').value = product.product_id;
  
  productNamePopup.style.display = 'none';
  console.log(product.product_id)
}

window.onclick = function (event) {
  if (!event.target.matches('.product-name-input')) {
    productNamePopup.style.display = 'none';
  }
};

tableBody.addEventListener('input', function (event) {
  if (event.target.matches('.product-name-input')) {
    showSuggestions(event.target)();
  } else if (event.target.matches('.qty-input') || event.target.matches('.amount-input') || event.target.matches('.discount-amount-input')) {
    calculateRow(event.target);
  }
});

// Add functionality to dynamically add rows
function addRow() {
  const lastRow = tableBody.lastElementChild;
  const newRow = lastRow.cloneNode(true);

  // Clear values in the new row
  newRow.querySelectorAll('input').forEach(input => input.value = '');
  newRow.querySelectorAll('.net-amount').forEach(span => span.textContent = '0.00');

  // Update sno in the new row
  const snoSpan = newRow.querySelector('.sno');
  snoSpan.textContent = parseInt(snoSpan.textContent) + 1;

  // Append the new row to the table body
  tableBody.appendChild(newRow);
}

// Function to handle click event on add row button
// document.getElementById('add-row-btn').addEventListener('click', addRow);

// Popup show

// SHOW DATA CONSOLE
// document.getElementById('payAmount').addEventListener('click', function() {
//   // Example tabular data
//   const tableData = [
//     { id: 1, name: 'John', age: 25 },
//     { id: 2, name: 'Jane', age: 30 },
//     { id: 3, name: 'Bob', age: 28 }
//   ];

//   // Convert tabular data to JSON format
//   const jsonData = JSON.stringify(tableData, null, 2);
//   console.log(jsonData)
//   // Display JSON data in the output div
//   // document.getElementById('output').innerText = jsonData;
// });


// 

// function selectAllRows() {
//   // Get the table element
//   const table = document.getElementById('product-table');

//   // Get all rows in the table body
//   const rows = table.getElementsByTagName('tbody')[0].getElementsByTagName('tr');

//   // Iterate through rows and set the "selected" class
//   for (let i = 0; i < rows.length; i++) {
//     rows[i].classList.add('selected');
//   }

//   // Log selected data to the console
//   logSelectedData();
// }

// function logSelectedData() {
//   // Get all rows with the "selected" class
//   const selectedRows = document.querySelectorAll('.selected');

//   // Log data for each selected row to the console
//   selectedRows.forEach(row => {
//     const rowData = Array.from(row.children).map(cell => cell.innerText);
//     console.log('Selected Row Data:', rowData);
//   });
// }

// 

// Define an array to store all data
const BillDetails = [];
// const CustomerDetailsArray = [];
const tableDataArray = [];
// const TableTotal = [];
const OverallDataArray = [];

// Define the logTableData function
function logTableData() {

  const Bill = {
    BillNo: document.getElementById('orderNumber').innerText,
    DateTimeP: document.getElementById('currentDateTime').innerText,
    GSTnum: document.getElementById('GSTon').innerText,
  }

  BillDetails.push(Bill);

  // Log the array to the console
  // console.log('Customer Data:', BillDetails);

  const customer = {
    CustomerName: document.getElementById('CustomerName').value,
    CustomerNumber: document.getElementById('CustomerNumber').value,
  };

  // Add the row data to the array
  // CustomerDetailsArray.push(customer);
  BillDetails.push(customer);

  // Log the array to the console
  // console.log('Customer Data:', CustomerDetailsArray);

  // Get all rows in the table body
  const rows = document.querySelectorAll('#product-table tbody .product-row');

  // Iterate through rows and build the array
  rows.forEach(row => {
    // Check if any input field in the row is filled
    const isRowFilled = Array.from(row.querySelectorAll('input')).some(input => input.value.trim() !== '');

    if (isRowFilled) {
      const rowData = {
        sno: row.querySelector('.sno').innerText,
        productName: row.querySelector('.product-name-input').value,
        hnsCode: row.querySelector('.HSN').value,
        qty: row.querySelector('.qty-input').value,
        sgstNo: row.querySelector('.sgst-no-input').value,
        cgstNo: row.querySelector('.CGST').value,
        amount: row.querySelector('.amount-input').value,
        discountAmount: row.querySelector('.discount-amount-input').value,
        netAmount: row.querySelector('.net-amount').innerText,
        product_id: row.querySelector('.pro_id').value
      };

      // Add the row data to the array
      tableDataArray.push(rowData);
    }
  });

  // Get data from tfoot (total row)
  const totalRowData = {
    sno: 'Total',
    productName: document.getElementById('product-list-length').innerText,
    hnsCode: document.getElementById('hns-code-total').value,
    qty: document.getElementById('qty-total').innerText,
    sgstNo: document.querySelector('.sgst-no-total').innerText,
    cgstNo: document.querySelector('.cgst-no-total').innerText,
    amount: document.getElementById('total-amount').innerText,
    discountAmount: document.getElementById('total-discount-amount').innerText,
    netAmount: document.getElementById('total-net-amount').innerText
  };

  // Add the total row data to the array
  // TableTotal.push(totalRowData);
  BillDetails.push(totalRowData);

  // Log the array to the console
  // console.log('table Data:', TableTotal);

  // Get data from Overall Details
  const OverallData = {
    SGST : document.getElementById('SGST').innerText,
    DisCount : document.getElementById('discount').innerText,
    Amount : document.getElementById('amount-input').value,
    CGST : document.getElementById('Cgst').innerText,
    Balance : document.getElementById('balance').innerText,
    GSTAmount : document.getElementById('gstAmount').innerText,
    DisAmount : document.getElementById('DiscountAmount').innerText,
    TotalAmount : document.getElementById('total').innerText
  }

  // Add the OverallData row data to the array
  // OverallDataArray.push(OverallData);
  BillDetails.push(OverallData)

  // Log the array to the console
  // console.log('Overall Total Data:', OverallDataArray);

  displayDataOnOutputPage();
  // updateDateTime()
  // updateOrderNumber();
  calculateRow();
}

// Example: Use onclick in HTML to call the logTableData function
// Example: <button onclick="logTableData()">Log Table Data</button>


//************************* SHOW OUTPUT OF TABLE DATA TO HTML PAGE WITH AUTO DOWNLOAD ******************//
// Function to create and display the output.html page
function displayDataOnOutputPage() {
  // Create HTML content
  const htmlContent = `
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Output Data</title>
    </head>
    <body>
      <h1>Bill Detail</h1>
      <pre>${JSON.stringify(BillDetails, null, 2)}</pre>
      <h1>Table Data</h1>
      <pre>${JSON.stringify(tableDataArray, null, 2)}</pre>
    </body>
    </html>
  `;

  // Create a Blob with the HTML content
  const blob = new Blob([htmlContent], { type: 'text/html' });

  // Create a link element
  const link = document.createElement('a');

  // Set the download attribute and the link's href to the Blob
  link.download = 'output.html';
  link.href = URL.createObjectURL(blob);

  // Append the link to the document body
  document.body.appendChild(link);

  // Click the link to trigger the download
  link.click();

  // Remove the link from the document body
  document.body.removeChild(link);
}

// *********************************** CUSTOMER DETAIL POPUP ************************************* //

  // Sample data (replace this with your actual data)
  // const customerData = [
  //   { name: 'Alice', number: '123' },
  //   { name: 'Andrew', number: '456' },
  //   // Add more customer data as needed
  // ];

  let selectedSuggestionIndex = -1;

  function showAutocomplete(input) {
    const popup = document.getElementById('autocomplete-popup');
    const customerDropdownInput = document.getElementById('CustomerName');
    const customerNumberInput = document.getElementById('CustomerNumber');

    // Clear previous results
    popup.innerHTML = '';

    // Filter customer names and numbers based on the entire input string
    const matchingCustomers = customerData.filter(customer =>
      customer.name.toLowerCase().includes(input.toLowerCase()) ||
      customer.number.includes(input) ||
      input.includes(customer.number)
    );

    // Display matching customer names and numbers in the popup
    matchingCustomers.forEach((customer, index) => {
      const suggestion = document.createElement('div');
      suggestion.classList.add('suggestion');
      suggestion.innerHTML = `<strong>${customer.name}</strong> - ${customer.number}`;
      suggestion.addEventListener('mousedown', (event) => {
        // Set selected customer name and number
        customerDropdownInput.value = customer.name;
        customerNumberInput.value = customer.number;
        // Hide the popup
        popup.style.display = 'none';
        // Prevent the input from losing focus
        event.preventDefault();
      });
      popup.appendChild(suggestion);
    });

    // Show the popup if there are matching suggestions
    popup.style.display = matchingCustomers.length > 0 ? 'block' : 'none';

    // Keyboard navigation with up and down arrows
    window.addEventListener('keydown', (event) => {
      if (event.key === 'ArrowUp' && selectedSuggestionIndex > 0) {
        selectedSuggestionIndex--;
      } else if (event.key === 'ArrowDown' && selectedSuggestionIndex < matchingCustomers.length - 1) {
        selectedSuggestionIndex++;
      } else if (event.key === 'Enter' && selectedSuggestionIndex !== -1) {
        // Fill in the customer name and number on Enter key press
        const selectedCustomer = matchingCustomers[selectedSuggestionIndex];
        customerDropdownInput.value = selectedCustomer.name;
        customerNumberInput.value = selectedCustomer.number;
        // Hide the popup
        popup.style.display = 'none';
      }

      // Update selected class
      const suggestions = document.querySelectorAll('.suggestion');
      suggestions.forEach((suggestion, index) => {
        if (index === selectedSuggestionIndex) {
          suggestion.classList.add('selected');
        } else {
          suggestion.classList.remove('selected');
        }
      });
    });
  }

  // Close the popup when clicking outside of it
  window.addEventListener('click', (event) => {
    const popup = document.getElementById('autocomplete-popup');
    const customerDropdownInput = document.getElementById('customerDropdown');

    if (event.target !== customerDropdownInput && event.target !== popup && !popup.contains(event.target)) {
      popup.style.display = 'none';
    }
  });

// *********************************** CURRENT DATE AND TIME ************************************* //
function updateDateTime() {
  // Get current date and time
  var currentDate = new Date();

  // Format the date and time as a string
  var formattedDateTime = currentDate.toLocaleString();

  // Display the formatted date and time in the HTML element with id "currentDateTime"
  document.getElementById("currentDateTime").textContent = formattedDateTime;

  console.log(formattedDateTime)
}

// Call the updateDateTime function when the page is loaded or refreshed
updateDateTime();

// *********************************** AUTO BILL NUMBER GENERATE ************************************* //

function updateOrderNumber() {
  // Check if the order number is stored in localStorage
  if (localStorage.getItem('orderNumber') === null) {
    // If not, initialize it to 1
    localStorage.setItem('orderNumber', '1');
  } else {
    // If yes, increment the order number
    var currentOrderNumber = parseInt(localStorage.getItem('orderNumber'));
    currentOrderNumber++;
    localStorage.setItem('orderNumber', currentOrderNumber.toString());
  }

  // Display the updated order number in the HTML element with id "orderNumber"
  document.getElementById("orderNumber").textContent = "SM 0" + localStorage.getItem('orderNumber');
}

// Call the updateOrderNumber function when the page is loaded or refreshed
updateOrderNumber();