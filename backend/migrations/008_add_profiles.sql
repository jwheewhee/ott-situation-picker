create table if not exists profiles (
    id uuid primary key references auth.users (id) on delete cascade,
    nickname text not null unique,
    avatar_id integer not null default 1 check (avatar_id between 1 and 10),
    created_at timestamptz not null default now()
);

alter table profiles enable row level security;

create policy "Profiles are viewable by everyone"
    on profiles for select
    using (true);

create policy "Users can insert their own profile"
    on profiles for insert
    with check (auth.uid() = id);

create policy "Users can update their own profile"
    on profiles for update
    using (auth.uid() = id);
