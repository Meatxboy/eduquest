import { Health } from "../types";

type Props = {
  health: Health;
};

export function HealthBar({ health }: Props) {
  const percentage = Math.max(0, Math.min(100, (health.current / health.max) * 100));

  return (
    <div className="card">
      <div className="header">
        <h2>Здоровье</h2>
        <strong>
          {health.current}/{health.max}
        </strong>
      </div>
      <div className="health-bar">
        <div className="health-fill" style={{ width: `${percentage}%` }} />
      </div>
    </div>
  );
}
