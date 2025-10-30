import { CompleteTaskResponse, UserState } from "./types";

const API_BASE_URL = import.meta.env.VITE_BACKEND_URL ?? "http://localhost:8000";

const headers = {
  "Content-Type": "application/json",
};

export async function initState(initData: string): Promise<UserState> {
  const response = await fetch(`${API_BASE_URL}/api/v1/auth/init`, {
    method: "POST",
    headers,
    body: JSON.stringify({ init_data: initData }),
  });

  if (!response.ok) {
    throw new Error("Не удалось инициализировать пользователя");
  }

  return (await response.json()) as UserState;
}

export async function fetchState(telegramId: number, username?: string | null): Promise<UserState> {
  const params = new URLSearchParams({ telegram_id: String(telegramId) });
  if (username) {
    params.set("username", username);
  }

  const response = await fetch(`${API_BASE_URL}/api/v1/state?${params.toString()}`);
  if (!response.ok) {
    throw new Error("Не удалось загрузить состояние пользователя");
  }

  return (await response.json()) as UserState;
}

export async function completeTask(
  telegramId: number,
  taskId: number,
  username?: string | null
): Promise<CompleteTaskResponse> {
  const params = new URLSearchParams({ telegram_id: String(telegramId) });
  if (username) {
    params.set("username", username);
  }

  const response = await fetch(`${API_BASE_URL}/api/v1/state/tasks/complete?${params.toString()}`, {
    method: "POST",
    headers,
    body: JSON.stringify({
      task_id: taskId,
      completed_at: new Date().toISOString(),
    }),
  });

  if (!response.ok) {
    throw new Error("Не удалось завершить задачу");
  }

  return (await response.json()) as CompleteTaskResponse;
}
