import { useEffect } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { AttributesGrid } from "./components/AttributesGrid";
import { ErrorBox } from "./components/ErrorBox";
import { GoalCard } from "./components/GoalCard";
import { HealthBar } from "./components/HealthBar";
import { LoadingScreen } from "./components/LoadingScreen";
import { ProgressCard } from "./components/ProgressCard";
import { EmptyTaskCard, TaskCard } from "./components/TaskCard";
import { completeTask, initState } from "./api";
import { useTelegram } from "./hooks/useTelegram";
import { UserState } from "./types";

function GoalsSection({ goals }: { goals: UserState["goals"] }) {
  return (
    <div className="card">
      <h2>Цели</h2>
      <div className="goals-grid">
        <GoalCard label="Вчера" goal={goals.yesterday} />
        <GoalCard label="Сегодня" goal={goals.today} />
        <GoalCard label="Завтра" goal={goals.tomorrow} />
      </div>
    </div>
  );
}

export default function App() {
  const queryClient = useQueryClient();
  const { initData, user, showAlert } = useTelegram();

  const stateQuery = useQuery<UserState, Error>({
    queryKey: ["user-state", user?.id],
    queryFn: async () => {
      if (!initData) {
        throw new Error("Нет initData");
      }
      return initState(initData);
    },
    enabled: Boolean(initData),
    retry: false,
  });

  useEffect(() => {
    if (stateQuery.error && showAlert) {
      showAlert(stateQuery.error.message);
    }
  }, [stateQuery.error, showAlert]);

  const completeTaskMutation = useMutation({
    mutationFn: (taskId: number) => {
      const currentState = queryClient.getQueryData<UserState>(["user-state", user?.id]);
      const telegramId = user?.id ?? currentState?.user_id;
      const username = user?.username ?? currentState?.username ?? undefined;
      if (!telegramId) {
        throw new Error("Не удалось определить пользователя");
      }
      return completeTask(telegramId, taskId, username);
    },
    onSuccess: (response) => {
      const key = ["user-state", user?.id ?? response.new_state.user_id];
      queryClient.setQueryData(key, response.new_state);
    },
    onError: (error: Error) => {
      showAlert?.(error.message ?? "Что-то пошло не так");
    },
  });

  if (stateQuery.isLoading || !user) {
    return <LoadingScreen />;
  }

  if (stateQuery.error) {
    return <ErrorBox>Ошибка: {stateQuery.error.message}</ErrorBox>;
  }

  const state = stateQuery.data;
  if (!state) {
    return <ErrorBox>Не удалось загрузить состояние пользователя.</ErrorBox>;
  }

  return (
    <div className="container">
      <header>
        <h1>EduQuest</h1>
        <p className="small-text">Привет, {user.username ?? `герой #${user.id}`}!</p>
      </header>

      <HealthBar health={state.health} />
      <ProgressCard progress={state.progress} />

      {state.current_task ? (
        <TaskCard
          task={state.current_task}
          onComplete={(taskId) => completeTaskMutation.mutate(taskId)}
          disabled={completeTaskMutation.isPending}
        />
      ) : (
        <EmptyTaskCard />
      )}

      <GoalsSection goals={state.goals} />
      <AttributesGrid attributes={state.attributes} />

      <footer className="small-text">Задач в очереди: {state.backlog_size}</footer>
    </div>
  );
}
