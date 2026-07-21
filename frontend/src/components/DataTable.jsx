function DataTable({ columns, data, emptyMessage, onRowClick, selectedId }) {
  if (!data || data.length === 0) return <div className="table-empty">{emptyMessage || "No records available."}</div>;
  return (
    <div className="table-wrapper">
      <table className="data-table">
        <thead><tr>{columns.map((column) => <th key={column.key}>{column.label}</th>)}</tr></thead>
        <tbody>
          {data.map((row, index) => (
            <tr key={`${row.id || row.employee_id || index}-${index}`} tabIndex={onRowClick ? 0 : undefined} className={`${onRowClick ? "clickable-row" : ""} ${selectedId === row.employee_id ? "selected-row" : ""}`} onClick={onRowClick ? () => onRowClick(row) : undefined} onKeyDown={onRowClick ? (event) => { if (event.key === "Enter" || event.key === " ") { event.preventDefault(); onRowClick(row); } } : undefined}>
              {columns.map((column) => <td key={column.key}>{column.render ? column.render(row) : row[column.key]}</td>)}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default DataTable;
