import database_common


@database_common.connection_handler
def get_questions(cursor):
    query = """
    SELECT * FROM question ORDER BY submission_time DESC
    """
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def get_answers(cursor):
    query = """
    SELECT * FROM answer ORDER BY submission_time DESC
    """
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def display_answer(cursor, id):
    query = """
    SELECT * FROM answer 
    WHERE question_id = %(id)s
    """
    cursor.execute(query, {'id': id})
    return cursor.fetchall()

@database_common.connection_handler
def get_single_question(cursor, id):
    query = """
    SELECT * FROM question WHERE id = %(id)s
    """
    cursor.execute(query, {'id': id})
    return cursor.fetchall()

@database_common.connection_handler
def add_new_answer(cursor, data):
    query = """
    INSERT INTO answer (submission_time,vote_number, question_id, message, image)
    VALUES (%s,%s,%s,%s,%s)
    """
    cursor.execute(query, data)
