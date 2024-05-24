// Get the table and the table body
const table = document.getElementById('portfolio-table');
const tableBody = document.getElementById('portfolio-data');

// Add event listeners for sorting
table.addEventListener('click', (event) => {
    if (event.target.tagName === 'TH') {
        const header = event.target;
        const sorted = !header.classList.contains('sorted');
        header.classList.toggle('sorted', sorted);

        // Sort the table data
        const data = [...tableBody.rows];
        const columnIndex = Array.from(header.parentNode.children).indexOf(header);
        data.sort((a, b) => {
            const aValue = parseFloat(a.cells[columnIndex].textContent.replace('%', ''));
            const bValue = parseFloat(b.cells[columnIndex].textContent.replace('%', ''));
            if (sorted) {
                return aValue - bValue;
            } else {
                return bValue - aValue;
            }
        });

        // Update the table body
        tableBody.innerHTML = '';
        data.forEach((row) => tableBody.appendChild(row));
    }
});
