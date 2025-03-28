from flask import Flask, request, Response
from flask_cors import CORS
from db import connect, disconnect

app = Flask(__name__)

CORS(app)

@app.route('/todos', methods=['GET', 'POST'])
def get_todos():
    db = connect()
    cursor = db.cursor(dictionary=True)

    if request.method == 'GET':
        sql = 'SELECT * FROM todos ORDER BY id DESC'
        cursor.execute(sql)

        todos = cursor.fetchall()

        disconnect(db)
        return todos

    if request.method == 'POST':
        title = request.json.get('title')
        description = request.json.get('description')
        due_date = request.json.get('due_date')
        completed = request.json.get('completed')
        category = request.json.get('category')

        # Dummy date formatter. The DB stores due_date in the following format YYYY-MM-DD.
        due_date = due_date[:10]
        params = title, description, due_date, completed, str(category)
        sql = '''
            INSERT INTO
                todos (id, title, description, due_date, completed, category_id)
            VALUES
                (NULL, %s, %s, %s, %s, %s)
        '''

        cursor.execute(sql, params)
        db.commit()

        disconnect(db)
        return {}


@app.route('/todos/<int:todo_id>', methods=['GET', 'DELETE', 'PUT'])
def handle_todo(todo_id):
    db = connect()
    cursor = db.cursor(dictionary=True)
    params = (todo_id, )

    if request.method == 'GET':
        sql = '''
            SELECT
                id, title, description, due_date, completed, category_id)
            FROM
                todos
            WHERE id = %s
        '''

        cursor.execute(sql, params)
        todo = cursor.fetchall()

        disconnect(db)
        return todo

    if request.method == 'PUT':
        pass

    if request.method == 'DELETE':
        sql = 'DELETE FROM todos WHERE id = %s'

        cursor.execute(sql, params)
        db.commit()

        disconnect(db)
        return Response('', status=200)


@app.route('/categories', methods=['GET'])
def get_categories():
    db = connect()
    cursor = db.cursor(dictionary=True)

    sql = 'SELECT * FROM categories'

    cursor.execute(sql)
    categories = cursor.fetchall()

    disconnect(db)
    return categories


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
