import { useMemo, useState } from "react";
import { KeyRound, Search, ShieldCheck, X } from "lucide-react";
import ErrorState from "../components/ErrorState";
import LoadingState from "../components/LoadingState";

function roleAccent(name = "") {
  const n = name.toLowerCase();
  if (n.includes("finance")) return "emerald";
  if (n.includes("hr")) return "rose";
  if (n.includes("help")) return "blue";
  if (n.includes("iam")) return "indigo";
  if (n.includes("security")) return "amber";
  if (n.includes("software") || n.includes("developer")) return "violet";
  return "blue";
}

function RolesPage({ roles, loading, error, onRetry }) {
  const [search, setSearch] = useState("");
  const [selected, setSelected] = useState(null);
  const filtered = useMemo(() => roles.filter((role) => `${role.job_title} ${(role.groups || []).join(" ")} ${(role.applications || []).join(" ")}`.toLowerCase().includes(search.toLowerCase())), [roles, search]);
  const active = selected || filtered[0];
  if (loading) return <LoadingState message="Loading role catalog..." />;
  if (error) return <ErrorState message={error} onRetry={onRetry} />;
  return (
    <div className="page-section">
      <div className="section-heading rich-heading"><div><p className="panel-label">Role Catalog</p><h2>Configured access profiles</h2><p className="section-meta">{filtered.length} of {roles.length} roles visible.</p></div><div className="count-chip"><ShieldCheck size={16} /> {roles.length} roles</div></div>
      <label className="filter-field search-field slim-search">Search roles<span><Search size={16} /><input type="search" value={search} onChange={(e) => setSearch(e.target.value)} placeholder="Search by title, group, or app..." /></span></label>
      <div className="role-catalog-layout"><div className="role-row-list">{filtered.map((role) => <button type="button" className={`role-row role-row-button role-accent-${roleAccent(role.job_title)} ${active?.job_title === role.job_title ? "selected" : ""}`} key={role.job_title} onClick={() => setSelected(role)}><KeyRound size={18} /><div className="role-row-main"><strong>{role.job_title}</strong><span>{role.groups?.length || 0} groups · {role.applications?.length || 0} applications</span></div><div className="chip-group">{(role.groups || []).slice(0, 2).map((g) => <span className="chip" key={g}>{g}</span>)}</div><div className="chip-group">{(role.applications || []).slice(0, 2).map((a) => <span className="chip app-chip" key={a}>{a}</span>)}</div></button>)}</div><aside className={`panel detail-panel ${active ? `role-accent-${roleAccent(active.job_title)}` : ""}`}>{active ? <><div className="role-detail-header"><div className="role-detail-icon"><KeyRound size={18} /></div><div><p className="panel-label">Role Detail</p><h2 className="role-title-accent">{active.job_title}</h2></div><button type="button" className="icon-button compact-close" onClick={() => setSelected(null)} aria-label="Clear role selection"><X size={16} /></button></div><div className="detail-grid metric-grid"><div><span>Groups</span><strong>{active.groups?.length || 0}</strong></div><div><span>Applications</span><strong>{active.applications?.length || 0}</strong></div></div><Section title="Groups" items={active.groups} /><Section title="Applications" items={active.applications} apps /></> : <p className="panel-note">No role selected.</p>}</aside></div>
    </div>
  );
}

function Section({ title, items = [], apps }) {
  return <div className="detail-section"><h3>{title}</h3><div className="chip-group">{items.map((item) => <span className={`chip ${apps ? "app-chip" : ""}`} key={item}>{item}</span>)}</div></div>;
}

export default RolesPage;
