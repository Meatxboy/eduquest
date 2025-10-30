export type Attribute = {
  name: string;
  value: number;
};

export type TaskDifficulty = "easy" | "medium" | "hard";
export type TaskStatus = "pending" | "in_progress" | "completed";

export type TaskPreview = {
  id: number;
  title: string;
  description?: string | null;
  difficulty: TaskDifficulty;
  status: TaskStatus;
  xp_reward: number;
  health_delta: number;
};

export type DailyGoalStatus = "pending" | "completed" | "missed";

export type DailyGoal = {
  id: number;
  date: string;
  title: string;
  description?: string | null;
  status: DailyGoalStatus;
};

export type Health = {
  current: number;
  max: number;
};

export type Progress = {
  level: number;
  experience: number;
  experience_in_level: number;
  experience_to_next_level: number;
  level_completion_percent: number;
};

export type GoalsBucket = {
  yesterday?: DailyGoal | null;
  today?: DailyGoal | null;
  tomorrow?: DailyGoal | null;
};

export type UserState = {
  user_id: number;
  username?: string | null;
  health: Health;
  progress: Progress;
  attributes: Attribute[];
  current_task?: TaskPreview | null;
  backlog_size: number;
  goals: GoalsBucket;
};

export type CompleteTaskResponse = {
  success: boolean;
  new_state: UserState;
};
