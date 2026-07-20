import { useEffect, useMemo, useState } from "react";
import { KeyRound, Search, ShieldCheck, X } from "lucide-react";
import { getRoles } from "../services/api";
import LoadingState from "../components/LoadingState";
import ErrorState from "../components/ErrorState";

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

function RolesPage() {
  const [roles, setRoles] = useState([]);
  const [search, setSearch] = useState("");
  const [selectedRole, setSelectedRole] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    getRoles()
      .then((response) => setRoles(response.roles || []))
      .catch((err) => setError(err.message || "Unable to load role catalog."))
      .finally(() => setLoading(false));
  }, []);

  const filteredRoles = useMemo(() => roles.filter((role) => `${role.job_title} ${(role.groups || []).join(" ")} ${(role.applications || []).join(" ")}`.toLowerCase().includes(search.toLowerCase())), [roles, search]);
  const activeRole = selectedRole || filteredRoles[0];

  if (loading) return <LoadingState message="Loading role catalog..." />;
  if (error) return <ErrorState message={error} onRetry={() => window.location.reload()} />;

  return (
    <div className="page-section">
      <div className="section-heading rich-heading">
        <div><p className="panel-label">Role Catalog</p><h2>Configured access profiles</h2><p className="section-meta">{filteredRoles.length} of {roles.length} roles visible.</p></div>
        <div className="count-chip"><ShieldCheck size={16} /> {roles.length} roles</div>
      </div>
      <label className="filter-field search-field slim-search">Search roles<span><Search size={16} /><input type="search" value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Search by title, group, or app..." /></span></label>
      <div className="role-catalog-layout">
        <div className="role-row-list">
          {filteredRoles.map((role) => (
            <button type="button" className={`role-row role-row-button role-accent-${getRoleAccent(role.job_title)} ${activeRole?.job_title === role.job_title ? "selected" : ""}`} key={role.job_title} onClick={() => setSelectedRole(role)}>
              <KeyRound size={18} aria-hidden="true" />
              <div className="role-row-main"><strong>{role.job_title}</strong><span>{role.groups?.length || 0} groups · {role.applications?.length || 0} applications</span></div>
              <div className="chip-group">{(role.groups || []).slice(0, 2).map((group) => <span className="chip" key={group}>{group}</span>)}</div>
              <div className="chip-group">{(role.applications || []).slice(0, 2).map((app) => <span className="chip app-chip" key={app}>{app}</span>)}</div>
            </button>
          ))}
        </div>
        <aside className={`panel detail-panel ${activeRole ? `role-accent-${getRoleAccent(activeRole.job_title)}` : ""}`}>
          {activeRole ? <><div className="role-detail-header"><div className="role-detail-icon"><KeyRound size={18} /></div><div><p className="panel-label">Role Detail</p><h2 className="role-title-accent">{activeRole.job_title}</h2></div><button type="button" className="icon-button compact-close" aria-label="Clear role selection" onClick={() => setSelectedRole(null)}><X size={16} /></button></div><div className="detail-grid metric-grid"><div><span>Groups</span><strong>{activeRole.groups?.length || 0}</strong></div><div><span>Applications</span><strong>{activeRole.applications?.length || 0}</strong></div></div><div className="detail-section"><h3>Groups</h3><div className="chip-group">{(activeRole.groups || []).map((group) => <span className="chip" key={group}>{group}</span>)}</div></div><div className="detail-section"><h3>Applications</h3><div className="chip-group">{(activeRole.applications || []).map((app) => <span className="chip app-chip" key={app}>{app}</span>)}</div></div></> : <p className="panel-note">No role selected.</p>}
        </aside>
      </div>
    </div>
  );
}

export default RolesPage;
