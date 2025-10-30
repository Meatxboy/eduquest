import clsx from "clsx";
import { TaskPreview } from "../types";

type Props = {
  task: TaskPreview;
  onComplete: (taskId: number) => void;
  disabled?: boolean;
};

const difficultyLabels: Record<TaskPreview["difficulty"], string> = {
  easy: "Легкая",
  medium: "Средняя",
  hard: "Сложная",
};

export function TaskCard({ task, onComplete, disabled }: Props) {
  return (
    <div className="card">
      <div className="badge">{difficultyLabels[task.difficulty]}</div>
      <h2 className="task-title">{task.title}</h2>
      {task.description && <p>{task.description}</p>}
      <div className="task-meta">
        <span>Опыт: +{task.xp_reward}</span>
        {task.health_delta !== 0 && <span>Здоровье: {task.health_delta}</span>}
      </div>
      <button className="cta-button" onClick={() => onComplete(task.id)} disabled={disabled}>
        Завершить задачу
      </button>
    </div>
  );
}

export function EmptyTaskCard() {
  return (
    <div className={clsx("card", "empty-state")}>На сегодня нет задач. Отличная работа!</div>
  );
}
