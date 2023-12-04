
    function calculateTotalRows(update) {
        // Get all tables on the page
        var tables = document.getElementsByTagName("table");
      
        // Initialize the total rows count
        var totalRows = 0;
      
        // Iterate through each table
        for (var i = 0; i < tables.length; i++) {
          // Get all rows in the current table
          var rows = tables[i].getElementsByTagName("tr");
      
          // Add the number of rows in the current table to the total
          totalRows += rows.length;
        }
        if (update) {
          document.getElementById("total").textContent = update;
        }
        // Update the content of the "total" span with the calculated totalRows
        document.getElementById("total").textContent = totalRows - 1;
      }
      
      // Call the function when the page is loaded
      window.onload = calculateTotalRows;
      //pagination------------
      let rowsPerPage = 10;
      
      // Function to handle pagination
      function showPage(pageNumber) {
        const table = document.getElementById("myTable");
        const spanRows = document.getElementById("rows");
      
        const rows = table.tBodies[0].rows;
      
        const startRow = (pageNumber - 1) * rowsPerPage + 1;
        const endRow = Math.min(pageNumber * rowsPerPage, rows.length);
      
        for (let i = 0; i < rows.length; i++) {
          rows[i].style.display = i >= startRow - 1 && i < endRow ? "" : "none";
        }
      
        // Update the content of the "rows" span
        spanRows.textContent = `${startRow} - ${endRow}`;
      }
      
      function setupPagination() {
        const table = document.getElementById("myTable");
        const rows = table.tBodies[0].rows;
        const paginationContainer = document.getElementById("pagination");
        const spanRows = document.getElementById("rows");
      
        // If the total number of rows is less than or equal to 10, display all rows
        if (rows.length <= rowsPerPage) {
          for (let i = 0; i < rows.length; i++) {
            rows[i].style.display = "";
          }
          spanRows.textContent = `1 - ${rows.length}`;
          paginationContainer.innerHTML = ""; // Clear pagination buttons
        } else {
          // Calculate the number of pages and generate pagination buttons
          const pageCount = Math.ceil(rows.length / rowsPerPage);
      
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
      
      // delete   rows
      function deleteSelectedRows() {
        var checkboxes = document.querySelectorAll(
          '#myTable tbody input[type="checkbox"]:checked'
        );
        console.log(checkboxes);
        var tableBody = document.getElementById("tablebody");
        var deletedRowsData = [];
        if (checkboxes.length === 0) {
          alert("please select any one");
          return;
        }
        // Ask for confirmation before deleting
        var isConfirmed = window.confirm(
          "Are you sure you want to delete the selected rows?"
        );
      
        if (!isConfirmed) {
          return; // Do nothing if not confirmed
        }
      
        checkboxes.forEach(function (checkbox) {
          // Assuming each checkbox is in a row, so we get the parent row
          var row = checkbox.closest("tr");
          if (row.style.display !== "none") {
            // Extract cell values from the row
            var rowData = {
              CategoryName: row.cells[1].innerText,
              CategoryCode: row.cells[2].innerText,
              Description: row.cells[3].innerText,
              Quantity: row.cells[4].innerText,
              Category_id: row.cells[6].innerText,
            };
      
            // Add the rowData to the array for later logging
            deletedRowsData.push(rowData);
      
            // Remove the row from the table body
            tableBody.removeChild(row);
          }
        });
       // console.log("Deleted Rows Data:", deletedRowsData);
        calculateTotalRows(deletedRowsData.length);
      
        changeRowsPerPage();
        console.log("Deleted Rows Data:", deletedRowsData);

fetch('{% url "category_delete_multiple" %}', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': '{{ csrf_token }}',
    },
    body: JSON.stringify({ category_ids: deletedRowsData }),
})
.then(response => response.json())
.then(data => {
    console.log('Response from server:', data);
})
.catch(error => {
    console.error('Error during fetch:', error);
});

        // Log the deleted rows' cell values to the console
        //console.log("Deleted Rows Data:", deletedRowsData);
      }
      function selectAllRows() {
        var checkboxes = document.querySelectorAll(
          '#myTable tbody input[type="checkbox"]'
        );
        var selectAllCheckbox = document.getElementById("selectall");
      
        checkboxes.forEach(function (checkbox) {
          checkbox.checked = selectAllCheckbox.checked;
        });
      }

