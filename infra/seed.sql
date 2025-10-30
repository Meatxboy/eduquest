INSERT INTO tasks (title, description, difficulty, xp_reward, health_delta)
VALUES
  ('Прочитать главу учебника', 'Погрузись в новую тему и сделай пометки', 'easy', 20, 0),
  ('Решить практические задания', 'Закрепи материал на практике', 'medium', 35, 0),
  ('Поделиться прогрессом с наставником', 'Опиши чему научился сегодня', 'easy', 15, 0)
ON CONFLICT DO NOTHING;
