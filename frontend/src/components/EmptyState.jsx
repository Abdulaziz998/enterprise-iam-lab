import { Inbox } from "lucide-react";

function EmptyState({ title, description, action }) {
  return <div className="empty-state"><Inbox className="empty-icon" size={24} aria-hidden="true" /><p className="empty-title">{title}</p><p className="empty-description">{description}</p>{action ? <div className="empty-action">{action}</div> : null}</div>;
}

export default EmptyState;
