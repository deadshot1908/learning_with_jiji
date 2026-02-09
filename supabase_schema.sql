-- PROFILES
create table profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  email text,
  created_at timestamp with time zone default now()
);

-- TOPICS
create table topics (
  id bigint generated always as identity primary key,
  name text not null unique,
  content text not null,
  created_at timestamp with time zone default now()
);

-- RESOURCES
create table resources (
  id bigint generated always as identity primary key,
  topic_id bigint references topics(id) on delete cascade,
  title text not null,
  type text check (type in ('ppt', 'video')),
  storage_url text not null,
  created_at timestamp with time zone default now()
);

-- QUERIES
create table queries (
  id bigint generated always as identity primary key,
  user_id uuid references profiles(id),
  query_text text not null,
  created_at timestamp with time zone default now()
);

-- ENABLE RLS
alter table profiles enable row level security;
alter table topics enable row level security;
alter table resources enable row level security;
alter table queries enable row level security;

-- RLS POLICIES
create policy "Public read topics"
on topics for select using (true);

create policy "Public read resources"
on resources for select using (true);

create policy "Users can read own profile"
on profiles for select using (auth.uid() = id);

create policy "Users can insert own queries"
on queries for insert with check (auth.uid() = user_id);

create policy "Users can read own queries"
on queries for select using (auth.uid() = user_id);
