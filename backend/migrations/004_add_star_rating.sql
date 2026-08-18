alter table content add column star_rating numeric check (star_rating between 1 and 5);
