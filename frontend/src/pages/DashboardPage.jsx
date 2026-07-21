import { Link } from "react-router-dom";
import { BadgeCheck, BookOpen, BriefcaseBusiness, ClipboardList, Database, Layers, ShieldCheck, UserRoundSearch, Users } from "lucide-react";
import DataTable from "../components/DataTable";
import EmptyState from "../components/EmptyState";
import ErrorState from "../components/ErrorState";
import LoadingState from "../components/LoadingState";
import StatusBadge from "../components/StatusBadge";

const pct = (count, total) => total ? Math.round((count / total) * 100) : 0;

function DashboardPage({ employees, roles, audits, loading, refreshing, error, onRetry, onSelectEmployee, onSeedDemo, onResetDemo }) {
  if (loading) return <LoadingState message="Loading dashboard data..." />;
  if (error) return <ErrorState message={error} onRetry={onRetry} />;
  const active = employees.filter((e) => String(e.status || "").toLowerCase() === "active").length;
  const terminated = employees.filter((e) => String(e.status || "").toLowerCase() === "terminated").length;
  const recentEmployees = employees.slice(0, 5);
  const recentAudits = audits.slice(0, 5);
  const roleDistribution = roles.slice(0, 6);
  const departmentRows = countBy(employees, "department");
  const roleRows = countBy(employees, "job_title");
  const auditSummary = {
    create: audits.filter((event) => event.action === "CREATE").length,
    update: audits.filter((event) => event.action === "UPDATE_ROLE").length,
    terminate: audits.filter((event) => event.action === "TERMINATE").length,
    success: audits.filter((event) => event.status === "SUCCESS").length,
    failed: audits.filter((event) => event.status === "FAILED").length,
  };

  return (
    <div className="dashboard-page">
      {refreshing ? <div className="refresh-strip">Refreshing IAM data...</div> : null}
      <div className="summary-grid">
        <Kpi icon={Users} label="Total Employees" count={employees.length} caption="Directory identities in scope." accent="blue" />
        <Kpi icon={BadgeCheck} label="Active Employees" count={active} caption={`${pct(active, employees.length)}% of workforce active.`} accent="green" />
        <Kpi icon={ShieldCheck} label="Configured Roles" count={roles.length} caption="RBAC profiles available." accent="indigo" />
        <Kpi icon={Layers} label="Audit Events" count={audits.length} caption="Lifecycle events recorded." accent="amber" />
      </div>
      <section className="quick-actions-panel"><div><p className="panel-label">Quick Actions</p><h2>Common administration views</h2></div><div className="quick-action-list"><Link className="quick-action-button" to="/employees"><UserRoundSearch size={16} /> View Employees</Link><Link className="quick-action-button" to="/roles"><ShieldCheck size={16} /> Browse Roles</Link><Link className="quick-action-button" to="/audit-logs"><ClipboardList size={16} /> Review Audit Logs</Link><a className="quick-action-button" href="http://127.0.0.1:8000/docs"><BookOpen size={16} /> Open API Docs</a></div></section>
      <section className="quick-actions-panel demo-panel"><div><p className="panel-label">Demo Environment</p><h2>Reviewer data controls</h2><p className="section-meta">Local/demo only. Roles are preserved.</p></div><div className="quick-action-list"><button type="button" className="quick-action-button" onClick={onSeedDemo}><Database size={16} /> Load Demo Data</button><button type="button" className="danger-button" onClick={onResetDemo}>Reset Demo Data</button></div></section>
      <div className="dashboard-grid">
        <section className="panel panel-small"><PanelTitle label="Workforce Status" title="Identity posture" /><div className="status-bars"><Bar label="Active employees" count={active} value={pct(active, employees.length)} /><Bar label="Terminated employees" count={terminated} value={pct(terminated, employees.length)} danger /></div></section>
        <section className="panel panel-small"><PanelTitle label="Role Coverage" title="Top configured roles" /><div className="coverage-list">{roleDistribution.map((role) => <div className="coverage-row" key={role.job_title}><BriefcaseBusiness size={16} /><div><strong>{role.job_title}</strong><span>{role.groups?.length || 0} groups · {role.applications?.length || 0} apps</span><div className="meter"><span style={{ width: `${Math.min(100, ((role.groups?.length || 0) + (role.applications?.length || 0)) * 20)}%` }} /></div></div></div>)}</div></section>
        <section className="panel panel-small"><PanelTitle label="Recent IAM Activity" title="Operational events" />{recentAudits.length ? <ul className="activity-list">{recentAudits.map((event, index) => <li key={`${event.timestamp}-${index}`}><span className="timeline-dot" /><div><p className="activity-action">{event.action}</p><p className="activity-detail">Employee {event.employee_id}</p></div><div><StatusBadge status={event.status} /><p className="activity-timestamp">{event.timestamp || "No timestamp"}</p></div></li>)}</ul> : <EmptyState title="No audit events" description="Lifecycle activity will appear here as the backend records events." action={<Link className="secondary-button" to="/audit-logs">Review Audit Logs</Link>} />}</section>
        <section className="panel panel-large"><PanelTitle label="Recent Employees" title="Latest directory records" /><DataTable columns={[{ key: "employee_id", label: "Employee ID" }, { key: "name", label: "Identity", render: (row) => `${row.first_name} ${row.last_name}` }, { key: "job_title", label: "Role" }, { key: "department", label: "Department" }, { key: "status", label: "Status", render: (row) => <StatusBadge status={row.status} /> }, { key: "username", label: "Username" }]} data={recentEmployees} emptyMessage="No employees available." onRowClick={onSelectEmployee} /></section>
      </div>
      <section className="analytics-grid">
        <AnalyticsPanel title="Department Distribution" rows={departmentRows} />
        <AnalyticsPanel title="Role Distribution" rows={roleRows} />
        <section className="panel panel-small"><PanelTitle label="Audit Activity Summary" title="Lifecycle outcomes" /><div className="audit-summary-grid"><Metric label="Create" value={auditSummary.create} /><Metric label="Role Updates" value={auditSummary.update} /><Metric label="Terminate" value={auditSummary.terminate} /><Metric label="Success" value={auditSummary.success} /><Metric label="Failed" value={auditSummary.failed} /></div></section>
      </section>
      <section className="panel panel-large"><PanelTitle label="Role Distribution" title="Configured role profile summary" /><div className="role-row-list">{roleDistribution.map((role) => <div className="role-row" key={role.job_title}><ShieldCheck size={18} /><div className="role-row-main"><strong>{role.job_title}</strong><span>{role.groups?.length || 0} groups · {role.applications?.length || 0} applications</span></div><div className="chip-group">{(role.groups || []).slice(0, 3).map((g) => <span className="chip" key={g}>{g}</span>)}</div><div className="chip-group">{(role.applications || []).slice(0, 3).map((a) => <span className="chip app-chip" key={a}>{a}</span>)}</div></div>)}</div></section>
    </div>
  );
}

function Kpi({ icon: Icon, label, count, caption, accent }) {
  return <article className={`stat-card accent-${accent}`}><div className="stat-card-head"><Icon className="stat-card-icon" size={18} /><span className="stat-card-label">{label}</span></div><p className="stat-card-count">{count}</p><p className="stat-card-caption">{caption}</p></article>;
}
function PanelTitle({ label, title }) { return <div className="panel-heading"><div><p className="panel-label">{label}</p><h2>{title}</h2></div></div>; }
function Bar({ label, count, value, danger }) { return <div className="status-bar-row"><span>{label}</span><strong>{count}</strong><div className={`meter ${danger ? "danger" : ""}`}><span style={{ width: `${value}%` }} /></div><small>{value}% of directory</small></div>; }
function countBy(items, key) {
  const counts = items.reduce((acc, item) => {
    const label = item[key] || "Unassigned";
    acc[label] = (acc[label] || 0) + 1;
    return acc;
  }, {});
  return Object.entries(counts).map(([label, count]) => ({ label, count })).sort((a, b) => b.count - a.count);
}
function AnalyticsPanel({ title, rows }) {
  const max = Math.max(...rows.map((row) => row.count), 1);
  return <section className="panel panel-small"><PanelTitle label="Analytics" title={title} /><div className="analytics-bars">{rows.length ? rows.map((row) => <div className="analytics-row" key={row.label}><div><strong>{row.label}</strong><span>{row.count}</span></div><div className="meter"><span style={{ width: `${Math.max(8, Math.round((row.count / max) * 100))}%` }} /></div></div>) : <p className="panel-note">No employee data available.</p>}</div></section>;
}
function Metric({ label, value }) {
  return <div className="metric-card"><span>{label}</span><strong>{value}</strong></div>;
}

export default DashboardPage;
