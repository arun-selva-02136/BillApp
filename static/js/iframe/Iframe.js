// Iframe Code
document.addEventListener('DOMContentLoaded', function () {
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.querySelector('.sidebar');
    const mainContent = document.querySelector('.main-content');

    sidebarToggle.addEventListener('click', function () {
        // Toggle sidebar visibility
        const isSidebarVisible = sidebar.style.marginLeft === '0px' || sidebar.style.marginLeft === '';
        sidebar.style.marginLeft = isSidebarVisible ? '-240px' : '0';

        // Adjust main content margin accordingly
        mainContent.style.marginLeft = isSidebarVisible ? '0' : '';
    });

    // Set the default page and style its button
    const defaultPageName = '../Dash-bord-Page/Dashbord.html';
    const defaultButton = document.querySelector(`button[onclick="showContent('${defaultPageName}')"]`);
    defaultButton.classList.add('active');
});

function showContent(pageName) {
    // Reset active state for all buttons
    document.querySelectorAll('.nav-link').forEach(btn => btn.classList.remove('active'));

    // Highlight the clicked button
    document.querySelector(`button[onclick="showContent('${pageName}')"]`).classList.add('active');

    // Load content in the iframe based on the button clicked
    const iframe = document.getElementById('content-iframe');
    iframe.src = `${pageName}`; // Assuming you have separate HTML files for each page
}
// Iframe Code