const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

async function fetchJson(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });
  const text = await response.text();
  const data = text ? JSON.parse(text) : {};
  if (!response.ok || data.success === false) {
    throw new Error(data.message || data.detail || response.statusText || "Request failed.");
  }
  return data;
}

function query(params) {
  const search = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => value && search.set(key, value));
  return search.toString() ? `?${search}` : "";
}

export const getEmployees = () => fetchJson("/employees");
export const getEmployee = (id) => fetchJson(`/employees/${encodeURIComponent(id)}`);
export const getRoles = () => fetchJson("/roles");
export const getAuditLogs = (filters = {}) => fetchJson(`/audit-logs${query(filters)}`);
export const createEmployee = (payload) => fetchJson("/employees", { method: "POST", body: JSON.stringify(payload) });
export const moveEmployee = (id, newJobTitle) => fetchJson(`/employees/${encodeURIComponent(id)}/move`, { method: "POST", body: JSON.stringify({ new_job_title: newJobTitle }) });
export const terminateEmployee = (id) => fetchJson(`/employees/${encodeURIComponent(id)}/terminate`, { method: "POST" });
export const getHealth = () => fetchJson("/health");
export const seedDemoData = () => fetchJson("/demo/seed", { method: "POST" });
export const resetDemoData = () => fetchJson("/demo/reset", { method: "POST" });
