import { NavLink } from "react-router-dom";
import { Activity, Layers, ScanFace, ServerCog, ShieldCheck, Users } from "lucide-react";

const navigation = [
  { label: "Overview", path: "/", icon: Activity },
  { label: "Employees", path: "/employees", icon: Users },
  { label: "Roles", path: "/roles", icon: ShieldCheck },
  { label: "Audit Logs", path: "/audit-logs", icon: Layers },
];

function Sidebar() {
  return (
    <aside className="sidebar" aria-label="Primary navigation">
      <div className="brand-panel">
        <div className="brand-mark" aria-hidden="true"><ScanFace size={21} /></div>
        <div><p className="brand-title">Enterprise IAM</p><p className="brand-subtitle">Identity Governance Console</p></div>
      </div>
      <nav className="sidebar-nav">
        {navigation.map((item) => {
          const Icon = item.icon;
          return <NavLink key={item.path} to={item.path} className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}><Icon className="nav-icon" size={18} /><span>{item.label}</span></NavLink>;
        })}
      </nav>
      <div className="sidebar-footer">
        <div className="footer-status"><span className="status-dot" aria-hidden="true" /><ServerCog className="footer-icon" size={16} /><div><p>API Connected</p><p className="footer-note">Local Development</p><p className="version-label">Enterprise IAM v1.0.0</p></div></div>
        <p className="builder-credit">Built by Abdulaziz Abdi</p>
      </div>
    </aside>
  );
}

export default Sidebar;
