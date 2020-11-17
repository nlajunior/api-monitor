use dbmonitor;

desc medicao;

select * from medicao where date_created in('2020-10-23');

create table organization (
 id integer not null auto_increment,
 date_created datetime default now(),
 secret_key varchar(300) not null,
 action_id varchar(100) not null,
 active boolean not null default 1,
 primary key(id)
 );
 
 create table actions (
  id integer not null auto_increment,
  name varchar(200) not null,
  active boolean not null default 1,
  primary key(id)
  );  

 create table test (
  id integer not null auto_increment,
  id_device varchar(200) not null,
  date_created datetime default now(),
  fhr_value integer not null,
  duration integer not null,
  active boolean not null default 1,
  organization_id integer,
  primary key(id)
  )