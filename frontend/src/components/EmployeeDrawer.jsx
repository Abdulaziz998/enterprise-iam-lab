import { BriefcaseBusiness, Fingerprint, KeyRound, Settings2, X } from "lucide-react";
import StatusBadge from "./StatusBadge";

function formatValue(value) {
  return value || "—";
}

function EmployeeDrawer({ employee, onClose, onMove, onTerminate }) {
  if (!employee) return null;
  const initials = `${employee.first_name?.[0] || ""}${employee.last_name?.[0] || ""}` || "ID";
  return (
    <div className="drawer-backdrop" role="presentation" onMouseDown={onClose}>
      <aside className="detail-drawer" role="dialog" aria-modal="true" aria-labelledby="employee-detail-title" onMouseDown={(event) => event.stopPropagation()}>
        <div className="drawer-header">
          <div className="identity-hero"><span className="drawer-avatar" aria-hidden="true">{initials}</span><div><p className="panel-label">Employee Detail</p><h2 id="employee-detail-title">{employee.first_name} {employee.last_name}</h2><div className="drawer-subline"><span>{employee.employee_id}</span><StatusBadge status={employee.status || "Unknown"} /></div></div></div>
          <button type="button" className="icon-button drawer-close" aria-label="Close employee details" onClick={onClose}><X size={17} /></button>
        </div>
        <div className="drawer-actions"><button type="button" className="secondary-button" onClick={() => onMove(employee)}><KeyRound size={16} /> Change Role</button><button type="button" className="danger-button" onClick={() => onTerminate(employee)}>Terminate Employee</button></div>
        <div className="detail-section"><h3><Fingerprint size={15} /> Identity</h3><div className="detail-grid"><div><span>Employee ID</span><strong>{formatValue(employee.employee_id)}</strong></div><div><span>Username</span><strong>{formatValue(employee.username)}</strong></div><div><span>First Name</span><strong>{formatValue(employee.first_name)}</strong></div><div><span>Last Name</span><strong>{formatValue(employee.last_name)}</strong></div></div></div>
        <div className="detail-section"><h3><BriefcaseBusiness size={15} /> Employment</h3><div className="detail-grid"><div><span>Department</span><strong>{formatValue(employee.department)}</strong></div><div><span>Role</span><strong>{formatValue(employee.job_title)}</strong></div><div><span>Manager</span><strong>{formatValue(employee.manager)}</strong></div><div><span>Status</span><strong>{formatValue(employee.status)}</strong></div></div></div>
        <div className="detail-section"><h3><KeyRound size={15} /> Access</h3><div className="access-stack"><div><span>Groups</span><div className="chip-group">{(employee.groups || []).length ? employee.groups.map((item) => <span className="chip" key={item}>{item}</span>) : <span className="panel-note">No groups assigned.</span>}</div></div><div><span>Applications</span><div className="chip-group">{(employee.applications || []).length ? employee.applications.map((item) => <span className="chip app-chip" key={item}>{item}</span>) : <span className="panel-note">No applications assigned.</span>}</div></div></div></div>
        <div className="detail-section"><h3><Settings2 size={15} /> System</h3><div className="detail-grid"><div><span>Created</span><strong>{formatValue(employee.created_at || employee.created || employee.created_date)}</strong></div><div><span>Updated</span><strong>{formatValue(employee.updated_at || employee.updated || employee.modified_at)}</strong></div></div></div>
      </aside>
    </div>
  );
}

export default EmployeeDrawer;
