drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  chat_id integer,
  message_id integer,
  title text not null,
  event_where text not null,
  event_when text not null,
  full_message text not null,
  author text not null,
  author_name text not null,
  author_username text not null
);

drop table if exists likes;
create table likes (
  id integer not null,
  person text not null,
  person_name text not null,
  person_username text not null
);

drop table if exists dislikes;
create table dislikes (
  id integer not null,
  person text not null,
  person_name text not null,
  person_username text not null
);

drop table if exists sent_invoices;
create table sent_invoices (
  id integer not null
);