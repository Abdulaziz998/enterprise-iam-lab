function StatCard({ icon: Icon, label, count, caption, trend, accent = "blue" }) {
  return (
    <div className={`stat-card accent-${accent}`}>
      <div className="stat-card-head">
        <Icon size={20} className="stat-card-icon" aria-hidden="true" />
        <span className="stat-card-label">{label}</span>
      </div>
      <p className="stat-card-count">{count}</p>
      <p className="stat-card-caption">{caption}</p>
      {trend ? <p className="stat-card-trend">{trend}</p> : null}
    </div>
  );
}

export default StatCard;
