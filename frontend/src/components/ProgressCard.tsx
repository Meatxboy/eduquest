import { Progress } from "../types";

type Props = {
  progress: Progress;
};

export function ProgressCard({ progress }: Props) {
  const percentage = Math.min(100, Math.round(progress.level_completion_percent));
  const levelCap = progress.experience_in_level + progress.experience_to_next_level;

  return (
    <div className="card">
      <div className="header">
        <h2>Прогресс</h2>
        <strong>Уровень {progress.level}</strong>
      </div>
      <div className="progress-bar" aria-label="прогресс до следующего уровня">
        <div className="progress-fill" style={{ width: `${percentage || 0}%` }} />
      </div>
      <p className="small-text">
        Опыт в уровне: {progress.experience_in_level} / {levelCap}
      </p>
    </div>
  );
}
