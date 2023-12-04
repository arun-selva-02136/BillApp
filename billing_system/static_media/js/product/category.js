//pagination------------
let rowsPerPage = 10;

// Function to handle pagination
function showPage(pageNumber) {
  const table = document.getElementById("myTable");
  document.getElementById("rows").innerText = rowsPerPage;
  const rows = table.tBodies[0].rows;

  for (let i = 0; i < rows.length; i++) {
    rows[i].style.display =
      i >= (pageNumber - 1) * rowsPerPage && i < pageNumber * rowsPerPage
        ? ""
        : "none";
  }
}

// Function to generate pagination buttons
function setupPagination() {
  const table = document.getElementById("myTable");
  const rows = table.tBodies[0].rows;
  const pageCount = Math.ceil(rows.length / rowsPerPage);
  const paginationContainer = document.getElementById("pagination");

  for (let i = 1; i <= pageCount; i++) {
    const button = document.createElement("button");
    button.textContent = i;
    button.addEventListener("click", function () {
      showPage(i);
    });
    paginationContainer.appendChild(button);
  }

  // Show the first page by default
  showPage(1);
}

// Function to change rows per page
function changeRowsPerPage() {
  const rowsPerPageSelect = document.getElementById("rowsPerPageSelect");
  rowsPerPage = parseInt(rowsPerPageSelect.value);

  // Re-setup pagination with the new number of rows per page
  const paginationContainer = document.getElementById("pagination");
  paginationContainer.innerHTML = "";
  setupPagination();
}

// Setup pagination on page load
window.addEventListener("load", setupPagination);

//-------------- paginationends------------

// ---------------search table data-----------
(function (document) {
  "use strict";

  var TableFilter = (function (myArray) {
    var search_input;

    function _onInputSearch(e) {
      search_input = e.target;
      var tables = document.getElementsByClassName(
        search_input.getAttribute("data-table")
      );
      myArray.forEach.call(tables, function (table) {
        myArray.forEach.call(table.tBodies, function (tbody) {
          myArray.forEach.call(tbody.rows, function (row) {
            var text_content = row.textContent.toLowerCase();
            var search_val = search_input.value.toLowerCase();
            row.style.display =
              text_content.indexOf(search_val) > -1 ? "" : "none";
          });
        });
      });
    }

    return {
      init: function () {
        var inputs = document.getElementsByClassName("search-input");
        myArray.forEach.call(inputs, function (input) {
          input.oninput = _onInputSearch;
        });
      },
    };
  })(Array.prototype);

  document.addEventListener("readystatechange", function () {
    if (document.readyState === "complete") {
      TableFilter.init();
    }
  });
})(document);

document.addEventListener("DOMContentLoaded", function (event) {
  var checkboxes = document.getElementsByName("funnel[]"),
    selectall = document.getElementById("selectall");

  for (var i = 0; i < checkboxes.length; i++) {
    checkboxes[i].addEventListener("change", function () {
      //Conver to array
      var inputList = Array.prototype.slice.call(checkboxes);

      //Set checked  property of selectall input
      selectall.checked = inputList.every(function (c) {
        return c.checked;
      });
    });
  }

  selectall.addEventListener("change", function () {
    for (var i = 0; i < checkboxes.length; i++) {
      checkboxes[i].checked = selectall.checked;
    }
  });
});
