import { useCallback, useEffect, useMemo, useState } from "react";
import { Route, Routes, useLocation } from "react-router-dom";
import AppShell from "./components/AppShell";
import EmployeeDrawer from "./components/EmployeeDrawer";
import { CreateEmployeeModal, MoveEmployeeModal, TerminateEmployeeModal } from "./components/EmployeeModals";
import { ToastProvider, useToast } from "./components/ToastProvider";
import DashboardPage from "./pages/DashboardPage";
import EmployeesPage from "./pages/EmployeesPage";
import RolesPage from "./pages/RolesPage";
import AuditLogsPage from "./pages/AuditLogsPage";
import { createEmployee, getAuditLogs, getEmployees, getRoles, moveEmployee, terminateEmployee } from "./services/api";

const routeMeta = {
  "/": { title: "Overview", description: "Executive summary of workforce and security operations." },
  "/employees": { title: "Employees", description: "Browse, create, and administer workforce identities." },
  "/roles": { title: "Roles", description: "Review RBAC role definitions and access group coverage." },
  "/audit-logs": { title: "Audit Logs", description: "Inspect recent IAM activity and operational events." },
};

function AppContent() {
  const location = useLocation();
  const page = routeMeta[location.pathname] || routeMeta["/"];
  const { notify } = useToast();
  const [employees, setEmployees] = useState([]);
  const [roles, setRoles] = useState([]);
  const [audits, setAudits] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [selectedEmployeeId, setSelectedEmployeeId] = useState(null);
  const [modal, setModal] = useState(null);
  const [refreshing, setRefreshing] = useState(false);

  const refreshAll = useCallback(async ({ quiet = false } = {}) => {
    if (!quiet) setLoading(true);
    setRefreshing(true);
    setError("");
    try {
      const [employeeResponse, roleResponse, auditResponse] = await Promise.all([getEmployees(), getRoles(), getAuditLogs()]);
      setEmployees(employeeResponse.employees || []);
      setRoles(roleResponse.roles || []);
      setAudits(auditResponse.events || []);
    } catch (err) {
      setError(err.message || "Unable to refresh IAM data.");
      notify({ type: "error", title: "Refresh failed", message: err.message });
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, [notify]);

  useEffect(() => { refreshAll(); }, [refreshAll]);
  const selectedEmployee = useMemo(() => employees.find((employee) => employee.employee_id === selectedEmployeeId), [employees, selectedEmployeeId]);

  const mutate = async (operation, successTitle) => {
    const result = await operation();
    await refreshAll({ quiet: true });
    notify({ type: "success", title: successTitle, message: result.message });
    return result;
  };

  const handleCreate = async (payload) => {
    await mutate(() => createEmployee(payload), "Employee created");
    setModal(null);
  };
  const handleMove = async (id, jobTitle) => {
    const result = await mutate(() => moveEmployee(id, jobTitle), "Role updated");
    setSelectedEmployeeId(result.employee?.employee_id || id);
    setModal(null);
  };
  const handleTerminate = async (id) => {
    const result = await mutate(() => terminateEmployee(id), "Employee terminated");
    setSelectedEmployeeId(result.employee?.employee_id || id);
    setModal(null);
  };

  return (
    <AppShell title={page.title} description={page.description} onCreateEmployee={() => setModal("create")}>
      <Routes>
        <Route path="/" element={<DashboardPage employees={employees} roles={roles} audits={audits} loading={loading} refreshing={refreshing} error={error} onRetry={refreshAll} onSelectEmployee={(employee) => setSelectedEmployeeId(employee.employee_id)} onCreateEmployee={() => setModal("create")} />} />
        <Route path="/employees" element={<EmployeesPage employees={employees} roles={roles} loading={loading} refreshing={refreshing} error={error} onRetry={refreshAll} selectedEmployeeId={selectedEmployeeId} onSelectEmployee={(employee) => setSelectedEmployeeId(employee.employee_id)} onCreateEmployee={() => setModal("create")} />} />
        <Route path="/roles" element={<RolesPage roles={roles} loading={loading} error={error} onRetry={refreshAll} />} />
        <Route path="/audit-logs" element={<AuditLogsPage initialAudits={audits} loading={loading} error={error} onRetry={refreshAll} />} />
        <Route path="*" element={<DashboardPage employees={employees} roles={roles} audits={audits} loading={loading} error={error} onRetry={refreshAll} onCreateEmployee={() => setModal("create")} />} />
      </Routes>
      <EmployeeDrawer employee={selectedEmployee} onClose={() => setSelectedEmployeeId(null)} onMove={() => setModal("move")} onTerminate={() => setModal("terminate")} />
      {modal === "create" ? <CreateEmployeeModal roles={roles} onClose={() => setModal(null)} onSubmit={handleCreate} /> : null}
      {modal === "move" && selectedEmployee ? <MoveEmployeeModal employee={selectedEmployee} roles={roles} onClose={() => setModal(null)} onSubmit={handleMove} /> : null}
      {modal === "terminate" && selectedEmployee ? <TerminateEmployeeModal employee={selectedEmployee} onClose={() => setModal(null)} onSubmit={handleTerminate} /> : null}
    </AppShell>
  );
}

function App() {
  return <ToastProvider><AppContent /></ToastProvider>;
}

export default App;
