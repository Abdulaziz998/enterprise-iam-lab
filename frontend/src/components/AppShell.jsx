import Sidebar from "./Sidebar";
import Topbar from "./Topbar";

function AppShell({ title, description, children }) {
  return (
    <div className="app-shell">
      <Sidebar />
      <main className="app-content">
        <Topbar title={title} description={description} />
        <section className="page-body">{children}</section>
      </main>
    </div>
  );
}

export default AppShell;
