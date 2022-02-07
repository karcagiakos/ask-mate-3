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
def list_answers(cursor, id):
    query = """
    SELECT * FROM answer 
    WHERE question_id = %(id)s
    """
    cursor.execute(query, {'id': id})
    return cursor.fetchall()

@database_common.connection_handler
def display_answer(cursor, id):
    query = """
    SELECT * FROM answer 
    WHERE  id = %(id)s
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

@database_common.connection_handler
def add_new_question(cursor, data):
    query = """
    INSERT INTO question (submission_time,view_number, vote_number, title, message, image)
    VALUES (%s,%s,%s,%s,%s,%s)
    """
    cursor.execute(query, data)

@database_common.connection_handler
def update_question(cursor, data):
    query = """
    UPDATE question
    SET title = %s, message = %s
    WHERE id = %s
    """
    cursor.execute(query,data)

@database_common.connection_handler
def delete_answer_with_question(cursor, id):
    query = """
    DELETE FROM answer
    WHERE question_id = %(id)s
    """
    cursor.execute(query, {'id': id})

@database_common.connection_handler
def delete_answer(cursor, id):
    query = """
    DELETE FROM answer
    WHERE id = %(id)s
    """
    cursor.execute(query, {'id': id})


@database_common.connection_handler
def delete_question(cursor, id):
    query = """
    DELETE FROM question
    WHERE id = %(id)s
    """
    cursor.execute(query, {'id': id})

@database_common.connection_handler
def delete_question_tag(cursor, id):
    query = """
    DELETE FROM question_tag
    WHERE question_id = %(id)s
    """
    cursor.execute(query, {'id': id})

@database_common.connection_handler
def delete_comment(cursor, id):
    query = """
    DELETE FROM comment
    WHERE question_id = %(id)s OR answer_id = %(id)s    """
    cursor.execute(query, {'id': id})