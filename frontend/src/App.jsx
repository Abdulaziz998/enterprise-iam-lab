import { Routes, Route, useLocation } from "react-router-dom";
import AppShell from "./components/AppShell";
import DashboardPage from "./pages/DashboardPage";
import EmployeesPage from "./pages/EmployeesPage";
import RolesPage from "./pages/RolesPage";
import AuditLogsPage from "./pages/AuditLogsPage";

const routeMeta = {
  "/": {
    title: "Overview",
    description: "Executive summary of workforce and security operations.",
  },
  "/employees": {
    title: "Employees",
    description: "Browse and filter the full identity directory.",
  },
  "/roles": {
    title: "Roles",
    description: "Review RBAC role definitions and access group coverage.",
  },
  "/audit-logs": {
    title: "Audit Logs",
    description: "Inspect recent IAM activity and operational events.",
  },
};

function App() {
  const location = useLocation();
  const page = routeMeta[location.pathname] || routeMeta["/"];

  return (
    <AppShell title={page.title} description={page.description}>
      <Routes>
        <Route path="/" element={<DashboardPage />} />
        <Route path="/employees" element={<EmployeesPage />} />
        <Route path="/roles" element={<RolesPage />} />
        <Route path="/audit-logs" element={<AuditLogsPage />} />
        <Route path="*" element={<DashboardPage />} />
      </Routes>
    </AppShell>
  );
}

export default App;
