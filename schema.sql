drop table if exists guests;
create table guests (
    id integer primary key autoincrement,
    first_name text not null,
    last_name text not null,
    email_address text not null
);
