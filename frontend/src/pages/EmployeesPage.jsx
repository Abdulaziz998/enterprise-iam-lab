import { useMemo, useState } from "react";
import { RotateCcw, Search, UserRoundCheck } from "lucide-react";
import DataTable from "../components/DataTable";
import ErrorState from "../components/ErrorState";
import LoadingState from "../components/LoadingState";
import StatusBadge from "../components/StatusBadge";
import { useToast } from "../components/ToastProvider";
import { dateStamp, downloadCsv } from "../services/csv";

const all = "All";
const uniq = (items, key) => [all, ...Array.from(new Set(items.map((item) => item[key]).filter(Boolean))).sort()];

function EmployeesPage({ employees, loading, refreshing, error, onRetry, onSelectEmployee, selectedEmployeeId, onCreateEmployee }) {
  const { notify } = useToast();
  const [search, setSearch] = useState("");
  const [status, setStatus] = useState(all);
  const [department, setDepartment] = useState(all);
  const [role, setRole] = useState(all);
  const filtered = useMemo(() => employees.filter((employee) => {
    const haystack = `${employee.employee_id} ${employee.first_name} ${employee.last_name} ${employee.department} ${employee.job_title} ${employee.username}`.toLowerCase();
    return (!search || haystack.includes(search.toLowerCase())) && (status === all || employee.status === status) && (department === all || employee.department === department) && (role === all || employee.job_title === role);
  }), [employees, search, status, department, role]);
  const reset = () => { setSearch(""); setStatus(all); setDepartment(all); setRole(all); };
  const exportEmployees = () => {
    try {
      downloadCsv(`employees-${dateStamp()}.csv`, [
        { label: "employee_id", value: (row) => row.employee_id },
        { label: "first_name", value: (row) => row.first_name },
        { label: "last_name", value: (row) => row.last_name },
        { label: "department", value: (row) => row.department },
        { label: "job_title", value: (row) => row.job_title },
        { label: "manager", value: (row) => row.manager },
        { label: "status", value: (row) => row.status },
        { label: "username", value: (row) => row.username },
      ], filtered);
      notify({ type: "success", title: "Employees exported", message: `${filtered.length} records downloaded.` });
    } catch (err) {
      notify({ type: "error", title: "Export failed", message: err.message });
    }
  };
  if (loading) return <LoadingState message="Loading employee directory..." />;
  if (error) return <ErrorState message={error} onRetry={onRetry} />;
  return (
    <div className="page-section">
      {refreshing ? <div className="refresh-strip">Refreshing employee list...</div> : null}
      <div className="section-heading rich-heading"><div><p className="panel-label">Directory</p><h2>Employee identity directory</h2><p className="section-meta">{filtered.length} of {employees.length} employees visible.</p></div><div className="heading-actions"><div className="count-chip"><UserRoundCheck size={16} /> {employees.length} total</div><button type="button" className="secondary-button" onClick={exportEmployees} disabled={!filtered.length}>Export Employees</button><button type="button" className="primary-button" onClick={onCreateEmployee}>Create Employee</button></div></div>
      <div className="filters-row toolbar">
        <label className="filter-field search-field">Search<span><Search size={16} /><input type="search" value={search} onChange={(e) => setSearch(e.target.value)} placeholder="Name, ID, role, department..." /></span></label>
        <Select label="Status" value={status} onChange={setStatus} options={uniq(employees, "status")} />
        <Select label="Department" value={department} onChange={setDepartment} options={uniq(employees, "department")} />
        <Select label="Role" value={role} onChange={setRole} options={uniq(employees, "job_title")} />
        <button type="button" className="secondary-button" onClick={reset}><RotateCcw size={16} /> Reset</button>
      </div>
      <DataTable selectedId={selectedEmployeeId} columns={[{ key: "employee_id", label: "Employee ID" }, { key: "name", label: "Identity", render: (row) => `${row.first_name} ${row.last_name}` }, { key: "job_title", label: "Role" }, { key: "department", label: "Department" }, { key: "manager", label: "Manager" }, { key: "status", label: "Status", render: (row) => <StatusBadge status={row.status} /> }, { key: "username", label: "Username" }]} data={filtered} emptyMessage="No employees match the selected filters." onRowClick={onSelectEmployee} />
    </div>
  );
}

function Select({ label, value, onChange, options }) {
  return <label className="filter-field">{label}<select value={value} onChange={(e) => onChange(e.target.value)}>{options.map((option) => <option key={option}>{option}</option>)}</select></label>;
}

export default EmployeesPage;
