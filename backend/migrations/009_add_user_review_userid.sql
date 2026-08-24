alter table user_review
    add column if not exists user_id uuid references auth.users (id) on delete set null;

create index if not exists idx_user_review_user_id on user_review (user_id);
