// Add sorting functionality
document.querySelectorAll('th').forEach(header => {
  header.addEventListener('click', () => {
    const table = header.closest('table');
    const rows = Array.from(table.querySelectorAll('tr:nth-child(n+2)'));
    const isNumeric = index => !isNaN(parseFloat(rows[0].children[index].textContent));
    
    rows.sort((a, b) => {
      const aValue = a.children[header.cellIndex].textContent;
      const bValue = b.children[header.cellIndex].textContent;
      
      if (isNumeric(header.cellIndex)) {
        return parseFloat(aValue) - parseFloat(bValue);
      }
      
      return aValue.localeCompare(bValue);
    });
    
    rows.forEach(row => table.appendChild(row));
  });
});
