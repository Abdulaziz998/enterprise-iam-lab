import { useEffect, useRef, useState } from "react";
import { Bell, CircleHelp, LogOut, Search, Settings } from "lucide-react";

function Topbar({ title, description, onCreateEmployee, onSearchOpen, onLogout, health }) {
  const [profileOpen, setProfileOpen] = useState(false);
  const ref = useRef(null);
  useEffect(() => {
    const onPointer = (event) => {
      if (ref.current && !ref.current.contains(event.target)) setProfileOpen(false);
    };
    const onKey = (event) => {
      if (event.key === "Escape") setProfileOpen(false);
    };
    document.addEventListener("mousedown", onPointer);
    document.addEventListener("keydown", onKey);
    return () => {
      document.removeEventListener("mousedown", onPointer);
      document.removeEventListener("keydown", onKey);
    };
  }, []);
  return (
    <div className="topbar">
      <div><p className="breadcrumb">Identity Governance / {title}</p><h1 className="page-title">{title}</h1><p className="page-description">{description}</p></div>
      <div className="topbar-actions">
        <button type="button" className="search-control search-trigger" onClick={onSearchOpen} aria-label="Open global search"><Search className="control-icon" size={17} aria-hidden="true" /><span>Search pages, roles, employees...</span><kbd>⌘K</kbd></button>
        <span className={`health-pill health-${health}`}>{health === "connected" ? "Connected" : health === "degraded" ? "Degraded" : "Offline"}</span>
        <button type="button" className="primary-button compact-action" onClick={onCreateEmployee}>Create Employee</button>
        <button type="button" className="icon-button" aria-label="Notifications"><span className="notification-dot" aria-hidden="true" /><Bell size={18} /></button>
        <button type="button" className="icon-button" aria-label="Help"><CircleHelp size={18} /></button>
        <button type="button" className="icon-button" aria-label="Settings"><Settings size={18} /></button>
        <div className="profile-menu-wrap" ref={ref}>
          <button type="button" className="profile-button" aria-label="Administrator profile" aria-expanded={profileOpen} onClick={() => setProfileOpen((value) => !value)}><span className="avatar-initials" aria-hidden="true">AA</span><span><strong>Abdulaziz Abdi</strong><small>Administrator</small></span></button>
          {profileOpen ? <div className="profile-menu" role="menu"><strong>Abdulaziz Abdi</strong><span>Administrator</span><span>Demo Environment</span><button type="button" role="menuitem" onClick={onLogout}><LogOut size={15} /> Logout</button></div> : null}
        </div>
      </div>
    </div>
  );
}

export default Topbar;
