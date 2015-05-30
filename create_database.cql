 CREATE KEYSPACE tornado_app
  WITH REPLICATION = 
{ 'class' : 'SimpleStrategy', 
  'replication_factor' : 2 };

use tornado_app;

CREATE TABLE todo_list (
  user_name text,
  id uuid,
  todo text,
  is_completed boolean,
  PRIMARY KEY((user_name), id)
);