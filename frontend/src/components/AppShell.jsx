import Sidebar from "./Sidebar";
import Topbar from "./Topbar";

function AppShell({ title, description, onCreateEmployee, children }) {
  return <div className="app-shell"><Sidebar /><main className="app-content"><Topbar title={title} description={description} onCreateEmployee={onCreateEmployee} /><section className="page-body">{children}</section></main></div>;
}

export default AppShell;
