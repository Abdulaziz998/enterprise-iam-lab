import { useEffect, useMemo, useState } from "react";
import { CheckCircle2, ChevronDown, ChevronRight, RotateCcw, Search, XCircle } from "lucide-react";
import { getAuditLogs } from "../services/api";
import LoadingState from "../components/LoadingState";
import ErrorState from "../components/ErrorState";
import StatusBadge from "../components/StatusBadge";
import EmptyState from "../components/EmptyState";

function formatTimestamp(value) {
  if (!value) return "No timestamp";
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? value : date.toLocaleString();
}

function getActionAccent(action = "") {
  const normalized = action.toUpperCase();
  if (normalized.includes("CREATE")) return "blue";
  if (normalized.includes("UPDATE_ROLE")) return "indigo";
  if (normalized.includes("TERMINATE")) return "red";
  return "amber";
}

function renderDetailRows(details) {
  if (!details) return [["Details", "No additional details."]];
  if (typeof details !== "object") return [["Details", String(details)]];
  const rows = Object.entries(details);
  return rows.length ? rows.map(([key, value]) => [key.replaceAll("_", " "), typeof value === "object" ? JSON.stringify(value) : String(value)]) : [["Details", "No additional details."]];
}

function AuditLogsPage() {
  const [auditLogs, setAuditLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({ action: "", status: "", employee_id: "" });
  const [expanded, setExpanded] = useState(null);

  const fetchLogs = (nextFilters = filters) => {
    setLoading(true);
    setError(null);
    getAuditLogs(nextFilters)
      .then((response) => setAuditLogs(response.events || []))
      .catch((err) => setError(err.message || "Unable to load audit logs."))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchLogs();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const actionOptions = useMemo(() => Array.from(new Set(auditLogs.map((event) => event.action).filter(Boolean))).sort(), [auditLogs]);
  const resetFilters = () => {
    const next = { action: "", status: "", employee_id: "" };
    setFilters(next);
    fetchLogs(next);
  };

  return (
    <div className="page-section">
      <div className="section-heading rich-heading">
        <div>
          <p className="panel-label">Audit Insights</p>
          <h2>IAM activity monitoring</h2>
          <p className="section-meta">{auditLogs.length} events returned from the audit API.</p>
        </div>
        <div className="count-chip">{auditLogs.length} events</div>
      </div>

      <div className="filters-row toolbar">
        <label className="filter-field">Action<select value={filters.action} onChange={(event) => setFilters({ ...filters, action: event.target.value })}><option value="">All actions</option>{actionOptions.map((action) => <option key={action}>{action}</option>)}</select></label>
        <label className="filter-field">Status<select value={filters.status} onChange={(event) => setFilters({ ...filters, status: event.target.value })}><option value="">All statuses</option><option>SUCCESS</option><option>FAILED</option></select></label>
        <label className="filter-field search-field">Employee ID<span><Search size={16} /><input type="text" value={filters.employee_id} onChange={(event) => setFilters({ ...filters, employee_id: event.target.value })} placeholder="100001" aria-label="Filter by employee ID" /></span></label>
        <button type="button" className="primary-button" onClick={() => fetchLogs()}>Apply</button>
        <button type="button" className="secondary-button" onClick={resetFilters}><RotateCcw size={16} /> Reset</button>
      </div>

      {loading ? (
        <LoadingState message="Loading audit activity..." />
      ) : error ? (
        <ErrorState message={error} onRetry={() => fetchLogs()} />
      ) : auditLogs.length === 0 ? (
        <EmptyState title="No audit activity found" description="Adjust the filters or retry when new lifecycle events are available." action={<button type="button" className="secondary-button" onClick={() => fetchLogs()}>Retry</button>} />
      ) : (
        <div className="audit-timeline">
          {auditLogs.map((event, index) => {
            const key = `${event.timestamp || index}-${event.employee_id}-${event.action}-${index}`;
            const isSuccess = String(event.status || "").toLowerCase() === "success";
            return (
              <article className={`audit-event action-${getActionAccent(event.action)}`} key={key}>
                <div className={`event-icon ${isSuccess ? "success" : "danger"}`}>{isSuccess ? <CheckCircle2 size={18} /> : <XCircle size={18} />}</div>
                <button type="button" className="event-main" onClick={() => setExpanded(expanded === key ? null : key)} aria-expanded={expanded === key}>
                  <span><strong>{event.action}</strong><small>{formatTimestamp(event.timestamp)}</small></span>
                  <span className="identity-pill">Employee {event.employee_id}</span>
                  <StatusBadge status={event.status || "Unknown"} />
                  {expanded === key ? <ChevronDown size={16} /> : <ChevronRight size={16} />}
                </button>
                {expanded === key ? <div className="event-details">{renderDetailRows(event.details).map(([label, value]) => <div className="detail-row" key={label}><span>{label}</span><strong>{value}</strong></div>)}</div> : null}
              </article>
            );
          })}
        </div>
      )}
    </div>
  );
}

export default AuditLogsPage;
