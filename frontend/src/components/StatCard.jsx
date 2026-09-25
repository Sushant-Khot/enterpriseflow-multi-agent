function StatCard({
  title,
  value,
  description,
  icon: Icon,
  type,
}) {

  return (
    <div className="stat-card">

      <div className="stat-top">

        <div className={`stat-icon ${type}`}>
          <Icon size={21} />
        </div>

        <span className="stat-label">
          {title}
        </span>

      </div>


      <div className="stat-value">
        {value}
      </div>


      <div className="stat-description">
        {description}
      </div>

    </div>
  );
}


export default StatCard;