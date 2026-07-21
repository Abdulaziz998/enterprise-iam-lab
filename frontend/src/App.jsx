import { useCallback, useEffect, useMemo, useState } from "react";
import { Navigate, Route, Routes, useLocation, useNavigate } from "react-router-dom";
import AppShell from "./components/AppShell";
import EmployeeDrawer from "./components/EmployeeDrawer";
import { CreateEmployeeModal, MoveEmployeeModal, TerminateEmployeeModal } from "./components/EmployeeModals";
import GlobalSearch from "./components/GlobalSearch";
import { ToastProvider, useToast } from "./components/ToastProvider";
import DashboardPage from "./pages/DashboardPage";
import EmployeesPage from "./pages/EmployeesPage";
import RolesPage from "./pages/RolesPage";
import AuditLogsPage from "./pages/AuditLogsPage";
import LoginPage from "./pages/LoginPage";
import { createEmployee, getAuditLogs, getEmployees, getHealth, getRoles, moveEmployee, resetDemoData, seedDemoData, terminateEmployee } from "./services/api";
import { clearDemoSession, getStoredSession } from "./services/auth";

const routeMeta = {
  "/": { title: "Overview", description: "Executive summary of workforce and security operations." },
  "/employees": { title: "Employees", description: "Browse, create, and administer workforce identities." },
  "/roles": { title: "Roles", description: "Review RBAC role definitions and access group coverage." },
  "/audit-logs": { title: "Audit Logs", description: "Inspect recent IAM activity and operational events." },
};

function AppContent() {
  const location = useLocation();
  const navigate = useNavigate();
  const page = routeMeta[location.pathname] || routeMeta["/"];
  const { notify } = useToast();
  const [session, setSession] = useState(() => getStoredSession());
  const [employees, setEmployees] = useState([]);
  const [roles, setRoles] = useState([]);
  const [audits, setAudits] = useState([]);
  const [health, setHealth] = useState("offline");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [selectedEmployeeId, setSelectedEmployeeId] = useState(null);
  const [modal, setModal] = useState(null);
  const [searchOpen, setSearchOpen] = useState(false);
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

  useEffect(() => { if (session) refreshAll(); }, [refreshAll, session]);
  useEffect(() => {
    if (!session) return;
    const check = async () => {
      try {
        const response = await getHealth();
        setHealth(response.status === "healthy" ? "connected" : "degraded");
      } catch {
        setHealth("offline");
      }
    };
    check();
    const id = window.setInterval(check, 30000);
    return () => window.clearInterval(id);
  }, [session]);
  useEffect(() => {
    const onKey = (event) => {
      if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") {
        event.preventDefault();
        setSearchOpen(true);
      }
    };
    document.addEventListener("keydown", onKey);
    return () => document.removeEventListener("keydown", onKey);
  }, []);
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
  const handleSeedDemo = async () => {
    const result = await mutate(() => seedDemoData(), "Demo data loaded");
    notify({ type: "info", title: "Demo environment", message: `${result.employees_created} employees prepared.` });
  };
  const handleResetDemo = async () => {
    if (!window.confirm("Reset demo data? This restores the local demo sample state.")) return;
    const result = await mutate(() => resetDemoData(), "Demo data reset");
    notify({ type: "warning", title: "Demo environment reset", message: `${result.employees_created} sample employees restored.` });
  };
  const handleLogout = () => {
    clearDemoSession();
    setSession(null);
    navigate("/login", { replace: true });
  };

  if (!session) {
    return (
      <Routes>
        <Route path="/login" element={<LoginPage onLogin={(nextSession) => { setSession(nextSession); navigate("/", { replace: true }); }} />} />
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    );
  }

  if (location.pathname === "/login") return <Navigate to="/" replace />;

  return (
    <AppShell title={page.title} description={page.description} onCreateEmployee={() => setModal("create")} onSearchOpen={() => setSearchOpen(true)} onLogout={handleLogout} health={health}>
      <Routes>
        <Route path="/" element={<DashboardPage employees={employees} roles={roles} audits={audits} loading={loading} refreshing={refreshing} error={error} onRetry={refreshAll} onSelectEmployee={(employee) => setSelectedEmployeeId(employee.employee_id)} onCreateEmployee={() => setModal("create")} onSeedDemo={handleSeedDemo} onResetDemo={handleResetDemo} />} />
        <Route path="/employees" element={<EmployeesPage employees={employees} roles={roles} loading={loading} refreshing={refreshing} error={error} onRetry={refreshAll} selectedEmployeeId={selectedEmployeeId} onSelectEmployee={(employee) => setSelectedEmployeeId(employee.employee_id)} onCreateEmployee={() => setModal("create")} />} />
        <Route path="/roles" element={<RolesPage roles={roles} loading={loading} error={error} onRetry={refreshAll} />} />
        <Route path="/audit-logs" element={<AuditLogsPage initialAudits={audits} loading={loading} error={error} onRetry={refreshAll} />} />
        <Route path="*" element={<DashboardPage employees={employees} roles={roles} audits={audits} loading={loading} error={error} onRetry={refreshAll} onCreateEmployee={() => setModal("create")} />} />
      </Routes>
      <EmployeeDrawer employee={selectedEmployee} onClose={() => setSelectedEmployeeId(null)} onMove={() => setModal("move")} onTerminate={() => setModal("terminate")} />
      {modal === "create" ? <CreateEmployeeModal roles={roles} onClose={() => setModal(null)} onSubmit={handleCreate} /> : null}
      {modal === "move" && selectedEmployee ? <MoveEmployeeModal employee={selectedEmployee} roles={roles} onClose={() => setModal(null)} onSubmit={handleMove} /> : null}
      {modal === "terminate" && selectedEmployee ? <TerminateEmployeeModal employee={selectedEmployee} onClose={() => setModal(null)} onSubmit={handleTerminate} /> : null}
      <GlobalSearch open={searchOpen} onClose={() => setSearchOpen(false)} employees={employees} roles={roles} audits={audits} onSelectEmployee={(employee) => setSelectedEmployeeId(employee.employee_id)} />
    </AppShell>
  );
}

function App() {
  return <ToastProvider><AppContent /></ToastProvider>;
}

export default App;
