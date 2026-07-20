import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { BadgeCheck, BookOpen, BriefcaseBusiness, ClipboardList, Layers, ShieldCheck, UserRoundSearch, Users } from "lucide-react";
import { getEmployees, getRoles, getAuditLogs } from "../services/api";
import StatCard from "../components/StatCard";
import StatusBadge from "../components/StatusBadge";
import LoadingState from "../components/LoadingState";
import ErrorState from "../components/ErrorState";
import EmptyState from "../components/EmptyState";

function getRoleAccent(roleName = "") {
  const normalized = roleName.toLowerCase();
  if (normalized.includes("finance")) return "emerald";
  if (normalized.includes("hr")) return "rose";
  if (normalized.includes("help")) return "blue";
  if (normalized.includes("iam")) return "indigo";
  if (normalized.includes("security")) return "amber";
  if (normalized.includes("software") || normalized.includes("developer")) return "violet";
  return "blue";
}

function formatTimestamp(value) {
  if (!value) return "No timestamp";
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? value : date.toLocaleString();
}

function DashboardPage() {
  const [employees, setEmployees] = useState([]);
  const [roles, setRoles] = useState([]);
  const [audits, setAudits] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    Promise.all([getEmployees(), getRoles(), getAuditLogs()])
      .then(([employeeResponse, roleResponse, auditResponse]) => {
        setEmployees(employeeResponse.employees || []);
        setRoles(roleResponse.roles || []);
        setAudits(auditResponse.events || []);
      })
      .catch((err) => setError(err.message || "Unable to load dashboard."))
      .finally(() => setLoading(false));
  }, []);

  const activeCount = useMemo(
    () => employees.filter((employee) => String(employee.status || "").toLowerCase() === "active").length,
    [employees]
  );
  const terminatedCount = useMemo(
    () => employees.filter((employee) => String(employee.status || "").toLowerCase() === "terminated").length,
    [employees]
  );
  const activePercent = employees.length ? Math.round((activeCount / employees.length) * 100) : 0;
  const terminatedPercent = employees.length ? Math.round((terminatedCount / employees.length) * 100) : 0;
  const recentEmployees = employees.slice(0, 5);
  const recentAudits = audits.slice(0, 5);
  const roleDistribution = roles.slice(0, 6);
  const maxCoverage = Math.max(
    ...roleDistribution.map((role) => (role.groups?.length || 0) + (role.applications?.length || 0)),
    1
  );

  if (loading) return <LoadingState message="Loading dashboard data..." />;
  if (error) return <ErrorState message={error} onRetry={() => window.location.reload()} />;

  return (
    <div className="dashboard-page">
      <div className="summary-grid">
        <StatCard icon={Users} label="Total Employees" count={employees.length} caption="Directory identities in scope." trend="Live from employee API" accent="blue" />
        <StatCard icon={BadgeCheck} label="Active Employees" count={activeCount} caption="Currently enabled identities." trend={`${activePercent}% of workforce active`} accent="green" />
        <StatCard icon={ShieldCheck} label="Configured Roles" count={roles.length} caption="RBAC profiles available." trend="Group and app coverage tracked" accent="indigo" />
        <StatCard icon={Layers} label="Audit Events" count={audits.length} caption="Lifecycle events recorded." trend="Latest operational telemetry" accent="amber" />
      </div>

      <section className="quick-actions-panel">
        <div>
          <p className="panel-label">Quick Actions</p>
          <h2>Common administration views</h2>
        </div>
        <div className="quick-action-list">
          <Link className="quick-action-button" to="/employees"><UserRoundSearch size={16} /> View Employees</Link>
          <Link className="quick-action-button" to="/roles"><ShieldCheck size={16} /> Browse Roles</Link>
          <Link className="quick-action-button" to="/audit-logs"><ClipboardList size={16} /> Review Audit Logs</Link>
          <a className="quick-action-button" href="http://127.0.0.1:8000/docs"><BookOpen size={16} /> Open API Docs</a>
        </div>
      </section>

      <div className="dashboard-grid">
        <section className="panel panel-small">
          <div className="panel-heading">
            <div>
              <p className="panel-label">Workforce Status</p>
              <h2>Identity posture</h2>
            </div>
          </div>
          <div className="status-bars">
            <div className="status-bar-row">
              <span>Active employees</span>
              <strong>{activeCount}</strong>
              <div className="meter"><span style={{ width: `${activePercent}%` }} /></div>
              <small>{activePercent}% of directory</small>
            </div>
            <div className="status-bar-row">
              <span>Terminated employees</span>
              <strong>{terminatedCount}</strong>
              <div className="meter danger"><span style={{ width: `${terminatedPercent}%` }} /></div>
              <small>{terminatedPercent}% of directory</small>
            </div>
          </div>
        </section>

        <section className="panel panel-small">
          <div className="panel-heading">
            <div>
              <p className="panel-label">Role Coverage</p>
              <h2>Top configured roles</h2>
            </div>
          </div>
          <div className="coverage-list">
            {roleDistribution.length ? roleDistribution.map((role) => {
              const coverage = (role.groups?.length || 0) + (role.applications?.length || 0);
              return (
                <div className={`coverage-row role-accent-${getRoleAccent(role.job_title)}`} key={role.job_title}>
                  <BriefcaseBusiness size={16} aria-hidden="true" />
                  <div>
                    <strong>{role.job_title}</strong>
                    <span>{role.groups?.length || 0} groups · {role.applications?.length || 0} apps</span>
                    <div className="meter"><span style={{ width: `${Math.max(10, Math.round((coverage / maxCoverage) * 100))}%` }} /></div>
                  </div>
                </div>
              );
            }) : <EmptyState title="No roles configured" description="Role coverage appears here once role data is available." />}
          </div>
        </section>

        <section className="panel panel-small">
          <div className="panel-heading">
            <div>
              <p className="panel-label">Recent IAM Activity</p>
              <h2>Operational events</h2>
            </div>
          </div>
          {recentAudits.length ? (
            <ul className="activity-list">
              {recentAudits.map((event) => (
                <li key={`${event.timestamp}-${event.employee_id}-${event.action}`}>
                  <span className="timeline-dot" aria-hidden="true" />
                  <div>
                    <p className="activity-action">{event.action}</p>
                    <p className="activity-detail">Employee {event.employee_id}</p>
                  </div>
                  <div>
                    <StatusBadge status={event.status} />
                    <p className="activity-timestamp">{formatTimestamp(event.timestamp)}</p>
                  </div>
                </li>
              ))}
            </ul>
          ) : <EmptyState title="No audit events" description="Lifecycle activity will appear here as the backend records events." action={<Link className="secondary-button" to="/audit-logs">Review Audit Logs</Link>} />}
        </section>

        <section className="panel panel-large">
          <div className="panel-heading">
            <div>
              <p className="panel-label">Recent Employees</p>
              <h2>Latest directory records</h2>
            </div>
          </div>
          <div className="table-wrapper">
            <table className="data-table compact-table">
              <thead><tr><th>Employee ID</th><th>Identity</th><th>Role</th><th>Department</th><th>Status</th><th>Username</th></tr></thead>
              <tbody>
                {recentEmployees.map((employee) => (
                  <tr key={employee.employee_id}>
                    <td>{employee.employee_id}</td>
                    <td>{`${employee.first_name} ${employee.last_name}`}</td>
                    <td>{employee.job_title}</td>
                    <td>{employee.department}</td>
                    <td><StatusBadge status={employee.status || "Unknown"} /></td>
                    <td>{employee.username}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      </div>

      <section className="panel panel-large">
        <div className="panel-heading">
          <div>
            <p className="panel-label">Role Distribution</p>
            <h2>Configured role profile summary</h2>
          </div>
        </div>
        <div className="role-row-list">
          {roleDistribution.map((role) => (
            <div className={`role-row role-accent-${getRoleAccent(role.job_title)}`} key={role.job_title}>
              <ShieldCheck size={18} aria-hidden="true" />
              <div className="role-row-main">
                <strong>{role.job_title}</strong>
                <span>{role.groups?.length || 0} groups · {role.applications?.length || 0} applications</span>
              </div>
              <div className="chip-group">{(role.groups || []).slice(0, 3).map((group) => <span className="chip" key={group}>{group}</span>)}</div>
              <div className="chip-group">{(role.applications || []).slice(0, 3).map((app) => <span className="chip app-chip" key={app}>{app}</span>)}</div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}

export default DashboardPage;
