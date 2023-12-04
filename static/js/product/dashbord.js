let barChart;  // Declare a variable to store the Chart instance

// Sample data for all months
const allMonthsData = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'July', 'Aug', 'Sep', 'Act', 'Nov', 'Dec'],
    sales: [12, 19, 3, 5, 2, 3, 0, 0, 0, 0, 0, 0],
    purchase: [-12, -19, -3, -5, -2, -3, 0, 0, 0, 0, 0, 0],
};

// Function to filter data based on the selected date range
function filterDataByDateRange(data, startDate, endDate) {
    const startMonth = startDate.getMonth();
    const endMonth = endDate.getMonth();

    const filteredData = {
        labels: data.labels.slice(startMonth, endMonth + 1),
        sales: data.sales.slice(startMonth, endMonth + 1),
        purchase: data.purchase.slice(startMonth, endMonth + 1),
    };

    return filteredData;
}

// Function to update the chart with new data
function updateChart() {
    // Destroy the existing chart instance if it exists
    if (barChart) {
        barChart.destroy();
    }

    const startDate = new Date(document.getElementById('startDate').value);
    const endDate = new Date(document.getElementById('endDate').value);

    // Filter data based on the selected date range
    const filteredData = filterDataByDateRange(allMonthsData, startDate, endDate);

    const ctx = document.getElementById('barChart').getContext('2d');
    barChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: filteredData.labels,
            datasets: [
                {
                    label: 'Sales',
                    data: filteredData.sales,
                    backgroundColor: 'rgb(15,167,4)',
                    borderWidth: 1,
                    borderRadius: 20,
                },
                {
                    label: 'Purchase',
                    data: filteredData.purchase,
                    backgroundColor: 'rgb(255,33,7)',
                    borderWidth: 1,
                    borderRadius: 20,
                }
            ]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true,
                        callback: function(value, index, values) {
                            return Math.abs(value);
                        }
                    }
                }],
                xAxes: [{
                    stacked: false,
                }]
            }
        }
    });
}

// Initial chart rendering
updateChart();