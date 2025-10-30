import { DailyGoal, DailyGoalStatus } from "../types";

type Props = {
  label: string;
  goal?: DailyGoal | null;
};

const goalStatusLabels: Record<DailyGoalStatus, string> = {
  pending: "В процессе",
  completed: "Выполнено",
  missed: "Пропущено",
};

export function GoalCard({ label, goal }: Props) {
  if (!goal) {
    return (
      <div className="goal-card">
        <h3>{label}</h3>
        <p className="small-text">Нет цели</p>
      </div>
    );
  }

  return (
    <div className="goal-card">
      <h3>{label}</h3>
      <strong>{goal.title}</strong>
      {goal.description && <p className="small-text">{goal.description}</p>}
      <div className="badge">{goalStatusLabels[goal.status]}</div>
    </div>
  );
}
