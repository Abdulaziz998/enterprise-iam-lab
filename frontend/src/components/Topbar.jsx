import { Bell, CircleHelp, Search, Settings } from "lucide-react";

function Topbar({ title, description }) {
  return (
    <div className="topbar">
      <div>
        <p className="breadcrumb">Identity Governance / {title}</p>
        <h1 className="page-title">{title}</h1>
        <p className="page-description">{description}</p>
      </div>

      <div className="topbar-actions">
        <label className="search-control">
          <Search className="control-icon" size={18} aria-hidden="true" />
          <input
            type="search"
            placeholder="Search pages, roles, employees..."
            aria-label="Search dashboard"
          />
        </label>
        <button type="button" className="icon-button" aria-label="Notifications">
          <span className="notification-dot" aria-hidden="true" />
          <Bell size={20} />
        </button>
        <button type="button" className="icon-button" aria-label="Help">
          <CircleHelp size={20} />
        </button>
        <button type="button" className="icon-button" aria-label="Settings">
          <Settings size={20} />
        </button>
        <button type="button" className="profile-button" aria-label="Administrator profile">
          <span className="avatar-initials" aria-hidden="true">AA</span>
          <span>
            <strong>Abdulaziz Abdi</strong>
            <small>Administrator</small>
          </span>
        </button>
      </div>
    </div>
  );
}

export default Topbar;
