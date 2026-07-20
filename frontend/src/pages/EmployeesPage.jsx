import { useEffect, useMemo, useState } from "react";
import { BriefcaseBusiness, Fingerprint, KeyRound, RotateCcw, Search, UserRoundCheck, X } from "lucide-react";
import { getEmployees } from "../services/api";
import DataTable from "../components/DataTable";
import StatusBadge from "../components/StatusBadge";
import LoadingState from "../components/LoadingState";
import ErrorState from "../components/ErrorState";

const allOption = "All";

function uniqueValues(items, key) {
  return [allOption, ...Array.from(new Set(items.map((item) => item[key]).filter(Boolean))).sort()];
}

function EmployeesPage() {
  const [employees, setEmployees] = useState([]);
  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState(allOption);
  const [departmentFilter, setDepartmentFilter] = useState(allOption);
  const [roleFilter, setRoleFilter] = useState(allOption);
  const [selectedEmployee, setSelectedEmployee] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    getEmployees()
      .then((response) => setEmployees(response.employees || []))
      .catch((err) => setError(err.message || "Unable to load employees."))
      .finally(() => setLoading(false));
  }, []);

  const statusOptions = uniqueValues(employees, "status");
  const departmentOptions = uniqueValues(employees, "department");
  const roleOptions = uniqueValues(employees, "job_title");

  const filteredEmployees = useMemo(() => employees.filter((employee) => {
    const haystack = `${employee.employee_id} ${employee.first_name} ${employee.last_name} ${employee.job_title} ${employee.department} ${employee.username}`.toLowerCase();
    return (!search || haystack.includes(search.toLowerCase()))
      && (statusFilter === allOption || String(employee.status || "") === statusFilter)
      && (departmentFilter === allOption || employee.department === departmentFilter)
      && (roleFilter === allOption || employee.job_title === roleFilter);
  }), [employees, search, statusFilter, departmentFilter, roleFilter]);

  const resetFilters = () => {
    setSearch("");
    setStatusFilter(allOption);
    setDepartmentFilter(allOption);
    setRoleFilter(allOption);
  };

  if (loading) return <LoadingState message="Loading employee directory..." />;
  if (error) return <ErrorState message={error} onRetry={() => window.location.reload()} />;

  return (
    <div className="page-section">
      <div className="section-heading rich-heading">
        <div>
          <p className="panel-label">Directory</p>
          <h2>Employee identity directory</h2>
          <p className="section-meta">{filteredEmployees.length} of {employees.length} employees visible.</p>
        </div>
        <div className="count-chip"><UserRoundCheck size={16} /> {employees.length} total</div>
      </div>

      <div className="filters-row toolbar">
        <label className="filter-field search-field">
          Search
          <span><Search size={16} /><input type="search" value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Name, ID, role, department..." aria-label="Search employees" /></span>
        </label>
        <label className="filter-field">Status<select value={statusFilter} onChange={(event) => setStatusFilter(event.target.value)}>{statusOptions.map((option) => <option key={option}>{option}</option>)}</select></label>
        <label className="filter-field">Department<select value={departmentFilter} onChange={(event) => setDepartmentFilter(event.target.value)}>{departmentOptions.map((option) => <option key={option}>{option}</option>)}</select></label>
        <label className="filter-field">Role<select value={roleFilter} onChange={(event) => setRoleFilter(event.target.value)}>{roleOptions.map((option) => <option key={option}>{option}</option>)}</select></label>
        <button type="button" className="secondary-button" onClick={resetFilters}><RotateCcw size={16} /> Reset</button>
      </div>

      <DataTable
        columns={[
          { key: "employee_id", label: "Employee ID" },
          { key: "name", label: "Identity", render: (row) => `${row.first_name} ${row.last_name}` },
          { key: "job_title", label: "Role" },
          { key: "department", label: "Department" },
          { key: "manager", label: "Manager" },
          { key: "status", label: "Status", render: (row) => <StatusBadge status={row.status || "Unknown"} /> },
          { key: "username", label: "Username" },
        ]}
        data={filteredEmployees}
        emptyMessage="No employees match the selected filters."
        onRowClick={setSelectedEmployee}
      />

      {selectedEmployee ? (
        <div className="drawer-backdrop" role="presentation" onClick={() => setSelectedEmployee(null)}>
          <aside className="detail-drawer" role="dialog" aria-modal="true" aria-labelledby="employee-detail-title" onClick={(event) => event.stopPropagation()}>
            <div className="drawer-header">
              <div className="identity-hero">
                <span className="drawer-avatar" aria-hidden="true">{`${selectedEmployee.first_name?.[0] || ""}${selectedEmployee.last_name?.[0] || ""}` || "ID"}</span>
                <div>
                  <p className="panel-label">Employee Detail</p>
                  <h2 id="employee-detail-title">{selectedEmployee.first_name} {selectedEmployee.last_name}</h2>
                  <div className="drawer-subline"><span>{selectedEmployee.employee_id}</span><StatusBadge status={selectedEmployee.status || "Unknown"} /></div>
                </div>
              </div>
              <button type="button" className="icon-button drawer-close" aria-label="Close employee details" onClick={() => setSelectedEmployee(null)}><X size={17} /></button>
            </div>
            <div className="detail-section"><h3><Fingerprint size={15} /> Identity</h3><div className="detail-grid"><div><span>Employee ID</span><strong>{selectedEmployee.employee_id || "—"}</strong></div><div><span>Username</span><strong>{selectedEmployee.username || "—"}</strong></div></div></div>
            <div className="detail-section"><h3><BriefcaseBusiness size={15} /> Employment</h3><div className="detail-grid"><div><span>Department</span><strong>{selectedEmployee.department || "—"}</strong></div><div><span>Role</span><strong>{selectedEmployee.job_title || "—"}</strong></div><div><span>Manager</span><strong>{selectedEmployee.manager || "—"}</strong></div><div><span>Status</span><strong>{selectedEmployee.status || "—"}</strong></div></div></div>
            <div className="detail-section"><h3><KeyRound size={15} /> Access</h3><div className="access-stack"><div><span>Groups</span><div className="chip-group">{(selectedEmployee.groups || []).map((item) => <span className="chip" key={item}>{item}</span>)}</div></div><div><span>Applications</span><div className="chip-group">{(selectedEmployee.applications || []).map((item) => <span className="chip app-chip" key={item}>{item}</span>)}</div></div></div></div>
          </aside>
        </div>
      ) : null}
    </div>
  );
}

export default EmployeesPage;
