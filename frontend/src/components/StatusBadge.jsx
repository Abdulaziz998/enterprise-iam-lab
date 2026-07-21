function StatusBadge({ status }) {
  const normalized = String(status || "unknown").toLowerCase();
  const variant = ["active", "success"].includes(normalized) ? "success" : ["terminated", "failed", "failure"].includes(normalized) ? "danger" : "warning";
  return <span className={`status-badge ${variant}`}>{status || "Unknown"}</span>;
}

export default StatusBadge;
