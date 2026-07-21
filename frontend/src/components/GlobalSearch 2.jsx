import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { FileClock, ShieldCheck, UserRound } from "lucide-react";

function GlobalSearch({ open, onClose, employees, roles, audits, onSelectEmployee }) {
  const [query, setQuery] = useState("");
  const [active, setActive] = useState(0);
  const navigate = useNavigate();
  const groups = useMemo(() => {
    const q = query.toLowerCase();
    const match = (text) => !q || String(text || "").toLowerCase().includes(q);
    return [
      { label: "Employees", icon: UserRound, items: employees.filter((e) => match(`${e.employee_id} ${e.first_name} ${e.last_name} ${e.department} ${e.job_title} ${e.username}`)).slice(0, 6), toResult: (e) => ({ id: `employee-${e.employee_id}`, title: `${e.first_name} ${e.last_name}`, meta: `${e.employee_id} · ${e.job_title}`, action: () => { navigate("/employees"); onSelectEmployee(e); } }) },
      { label: "Roles", icon: ShieldCheck, items: roles.filter((r) => match(`${r.job_title} ${(r.groups || []).join(" ")} ${(r.applications || []).join(" ")}`)).slice(0, 5), toResult: (r) => ({ id: `role-${r.job_title}`, title: r.job_title, meta: `${r.groups?.length || 0} groups · ${r.applications?.length || 0} apps`, action: () => navigate("/roles") }) },
      { label: "Audit Events", icon: FileClock, items: audits.filter((a) => match(`${a.action} ${a.employee_id} ${a.status} ${JSON.stringify(a.details || {})}`)).slice(0, 5), toResult: (a, i) => ({ id: `audit-${a.timestamp}-${i}`, title: a.action, meta: `Employee ${a.employee_id} · ${a.status}`, action: () => navigate("/audit-logs") }) },
    ];
  }, [audits, employees, navigate, onSelectEmployee, query, roles]);
  const results = groups.flatMap((group) => group.items.map(group.toResult));

  useEffect(() => {
    if (!open) return;
    setQuery("");
    setActive(0);
    const onKeyDown = (event) => {
      if (event.key === "Escape") onClose();
      if (event.key === "ArrowDown") { event.preventDefault(); setActive((index) => Math.min(results.length - 1, index + 1)); }
      if (event.key === "ArrowUp") { event.preventDefault(); setActive((index) => Math.max(0, index - 1)); }
      if (event.key === "Enter" && results[active]) { results[active].action(); onClose(); }
    };
    document.addEventListener("keydown", onKeyDown);
    return () => document.removeEventListener("keydown", onKeyDown);
  }, [active, onClose, open, results]);

  if (!open) return null;
  let resultIndex = -1;
  return (
    <div className="search-backdrop" role="presentation" onMouseDown={onClose}>
      <section className="search-dialog" role="dialog" aria-modal="true" aria-label="Global search" onMouseDown={(e) => e.stopPropagation()}>
        <input autoFocus value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Search employees, roles, and audit events..." aria-label="Search query" />
        <div className="search-results">
          {groups.map((group) => {
            const Icon = group.icon;
            if (!group.items.length) return null;
            return <div className="search-group" key={group.label}><p><Icon size={15} /> {group.label}</p>{group.items.map((item, itemIndex) => { const result = group.toResult(item, itemIndex); resultIndex += 1; const index = resultIndex; return <button type="button" className={index === active ? "active" : ""} key={result.id} onMouseEnter={() => setActive(index)} onClick={() => { result.action(); onClose(); }}><strong>{result.title}</strong><span>{result.meta}</span></button>; })}</div>;
          })}
          {!results.length ? <p className="panel-note">No live records match this search.</p> : null}
        </div>
      </section>
    </div>
  );
}

export default GlobalSearch;
