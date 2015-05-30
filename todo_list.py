from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application, url
import uuid
from cassandra.cluster import Cluster

# note: without defining parameters Cluster() connects to localhost
cassandra_cluster = Cluster()

# note: you don't have to provide a keyspace argument below
# but then you'd have to specify it in every query
session = cassandra_cluster.connect('tornado_app')

class ToDoList(RequestHandler):
    # To set up a more meaningful example for the database, 
    # hard code a user to skip creating login capabilities
    user_name = "DePy2015"

    def get(self):
        rows = session.execute('SELECT id, todo, is_completed FROM todo_list WHERE user_name = %s', (self.user_name,))
        self.render("todo_list.html", user_name=self.user_name, todo_list=rows)

    def post(self):
        new_todo = self.get_argument('new_todo', '')
        session.execute("INSERT INTO todo_list (user_name, id, todo, is_completed) VALUES (%s, %s, %s, %s)", (self.user_name, uuid.uuid1(), new_todo, False))
        self.redirect('/')

    def put(self):
        todo_id = uuid.UUID(self.get_argument('todo_id', ''))
        is_completed = True if self.get_argument('is_completed_status', '')==u'true' else False
        session.execute("UPDATE todo_list SET is_completed = %s WHERE id = %s AND user_name = %s", (is_completed, todo_id, self.user_name))
        self.finish()

    def delete(self):
        todo_id = uuid.UUID(self.get_argument('todo_id', ''))
        session.execute("DELETE FROM todo_list WHERE id = %s AND user_name = %s", (todo_id, self.user_name))
        self.finish()


def make_app(database_session):
    return Application([
        url(r"/", ToDoList),
        ])

def main():
    app = make_app(session)
    app.listen(8888)
    IOLoop.current().start()

if __name__ == "__main__":
	main()

