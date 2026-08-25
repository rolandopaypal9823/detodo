-- ============================================================
-- FOCUS · Habit Tracker NFM — esquema Supabase
-- Correr una sola vez en el SQL Editor del proyecto.
-- ============================================================

-- Una fila por usuario con todo su estado (hábitos, marcas, objetivos).
-- Simple, suficiente para el MVP, y fácil de normalizar más adelante.
create table if not exists public.user_data (
  user_id    uuid primary key references auth.users (id) on delete cascade,
  data       jsonb not null default '{}'::jsonb,
  updated_at timestamptz not null default now()
);

alter table public.user_data enable row level security;

-- Cada usuario ve y escribe SOLO su propia fila.
create policy "own data - select" on public.user_data
  for select using (auth.uid() = user_id);

create policy "own data - insert" on public.user_data
  for insert with check (auth.uid() = user_id);

create policy "own data - update" on public.user_data
  for update using (auth.uid() = user_id) with check (auth.uid() = user_id);

create policy "own data - delete" on public.user_data
  for delete using (auth.uid() = user_id);
