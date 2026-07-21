import { useEffect, useMemo, useState } from "react";
import { CheckCircle2, ChevronDown, ChevronRight, RotateCcw, Search, XCircle } from "lucide-react";
import EmptyState from "../components/EmptyState";
import ErrorState from "../components/ErrorState";
import LoadingState from "../components/LoadingState";
import StatusBadge from "../components/StatusBadge";
import { useToast } from "../components/ToastProvider";
import { getAuditLogs } from "../services/api";
import { dateStamp, downloadCsv } from "../services/csv";

function rows(details) {
  if (!details) return [["Details", "No additional details."]];
  if (typeof details !== "object") return [["Details", String(details)]];
  return Object.entries(details).map(([k, v]) => [k.replaceAll("_", " "), typeof v === "object" ? JSON.stringify(v) : String(v)]);
}
function actionAccent(action = "") {
  const a = action.toUpperCase();
  if (a.includes("CREATE")) return "blue";
  if (a.includes("UPDATE_ROLE")) return "indigo";
  if (a.includes("TERMINATE")) return "red";
  return "amber";
}

function AuditLogsPage({ initialAudits, loading: initialLoading, error: initialError, onRetry }) {
  const { notify } = useToast();
  const [logs, setLogs] = useState(initialAudits || []);
  const [loading, setLoading] = useState(initialLoading);
  const [error, setError] = useState(initialError);
  const [filters, setFilters] = useState({ action: "", status: "", employee_id: "" });
  const [expanded, setExpanded] = useState(null);
  useEffect(() => setLogs(initialAudits || []), [initialAudits]);
  const actionOptions = useMemo(() => Array.from(new Set(logs.map((e) => e.action).filter(Boolean))).sort(), [logs]);
  const fetchLogs = async (next = filters) => { setLoading(true); setError(""); try { const data = await getAuditLogs(next); setLogs(data.events || []); } catch (err) { setError(err.message); } finally { setLoading(false); } };
  const reset = () => { const next = { action: "", status: "", employee_id: "" }; setFilters(next); fetchLogs(next); };
  const exportAudits = () => {
    try {
      downloadCsv(`audit-logs-${dateStamp()}.csv`, [
        { label: "timestamp", value: (row) => row.timestamp },
        { label: "action", value: (row) => row.action },
        { label: "employee_id", value: (row) => row.employee_id },
        { label: "status", value: (row) => row.status },
        { label: "details", value: (row) => row.details },
      ], logs);
      notify({ type: "success", title: "Audit logs exported", message: `${logs.length} records downloaded.` });
    } catch (err) {
      notify({ type: "error", title: "Export failed", message: err.message });
    }
  };
  return (
    <div className="page-section">
      <div className="section-heading rich-heading"><div><p className="panel-label">Audit Insights</p><h2>IAM activity monitoring</h2><p className="section-meta">{logs.length} events returned from the audit API.</p></div><div className="heading-actions"><div className="count-chip">{logs.length} events</div><button type="button" className="secondary-button" onClick={exportAudits} disabled={!logs.length}>Export Audit Logs</button></div></div>
      <div className="filters-row toolbar"><label className="filter-field">Action<select value={filters.action} onChange={(e) => setFilters({ ...filters, action: e.target.value })}><option value="">All actions</option>{actionOptions.map((a) => <option key={a}>{a}</option>)}</select></label><label className="filter-field">Status<select value={filters.status} onChange={(e) => setFilters({ ...filters, status: e.target.value })}><option value="">All statuses</option><option>SUCCESS</option><option>FAILED</option></select></label><label className="filter-field search-field">Employee ID<span><Search size={16} /><input value={filters.employee_id} onChange={(e) => setFilters({ ...filters, employee_id: e.target.value })} placeholder="100001" /></span></label><button type="button" className="primary-button" onClick={() => fetchLogs()}>Apply</button><button type="button" className="secondary-button" onClick={reset}><RotateCcw size={16} /> Reset</button></div>
      {loading ? <LoadingState message="Loading audit activity..." /> : error ? <ErrorState message={error} onRetry={onRetry || (() => fetchLogs())} /> : logs.length === 0 ? <EmptyState title="No audit activity found" description="Adjust filters or retry when new lifecycle events are available." action={<button type="button" className="secondary-button" onClick={() => fetchLogs()}>Retry</button>} /> : <div className="audit-timeline">{logs.map((event, index) => { const key = `${event.timestamp || index}-${event.employee_id}-${event.action}-${index}`; const ok = String(event.status || "").toLowerCase() === "success"; return <article className={`audit-event action-${actionAccent(event.action)}`} key={key}><div className={`event-icon ${ok ? "success" : "danger"}`}>{ok ? <CheckCircle2 size={18} /> : <XCircle size={18} />}</div><button type="button" className="event-main" onClick={() => setExpanded(expanded === key ? null : key)} aria-expanded={expanded === key}><span><strong>{event.action}</strong><small>{event.timestamp || "No timestamp"}</small></span><span className="identity-pill">Employee {event.employee_id}</span><StatusBadge status={event.status} />{expanded === key ? <ChevronDown size={16} /> : <ChevronRight size={16} />}</button>{expanded === key ? <div className="event-details">{rows(event.details).map(([label, value]) => <div className="detail-row" key={label}><span>{label}</span><strong>{value}</strong></div>)}</div> : null}</article>; })}</div>}
    </div>
  );
}

export default AuditLogsPage;
