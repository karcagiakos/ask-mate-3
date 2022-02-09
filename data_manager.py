import database_common
import psycopg2

# psycopg2 module psycopg2.sql literal
# psycopg2 module psycopg2.sql Idetifier

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
def delete_comment(cursor, id):
    query = """
    DELETE FROM comment
    WHERE  id = %(id)s   """
    cursor.execute(query, {'id': id})


@database_common.connection_handler
def update_answer_vote(cursor,id,amount):
    query = """
    UPDATE answer
    SET vote_number = vote_number + %(amount)s
    WHERE id = %(id)s"""
    cursor.execute(query, {'id': id, 'amount': amount})


@database_common.connection_handler
def update_question_vote(cursor,id,amount):
    query = """
    UPDATE question
    SET vote_number = vote_number + %(amount)s
    WHERE id = %(id)s"""
    cursor.execute(query, {'id': id, 'amount': amount})\


@database_common.connection_handler
def update_view_number(cursor,id):
    query = """
    UPDATE question
    SET view_number = view_number + 1
    WHERE id = %(id)s"""
    cursor.execute(query, {'id': id})

@database_common.connection_handler
def get_comments_for_questions(cursor,id):
    query= """
    SELECT message,submission_time, id, edited_count FROM comment WHERE question_id = %(id)s
    """
    cursor.execute(query, {'id': id})
    return cursor.fetchall()

@database_common.connection_handler
def get_comments_for_answers(cursor,id):
    query= """
    SELECT message,submission_time, id, edited_count FROM comment WHERE answer_id = %(id)s
    """
    cursor.execute(query, {'id': id})
    return cursor.fetchall()


@database_common.connection_handler
def add_new_comment_question(cursor, data):
    query = """
    INSERT INTO comment (question_id,message,submission_time, edited_count)
    VALUES (%s,%s,%s,%s)
    """
    cursor.execute(query, data)


@database_common.connection_handler
def add_new_comment_answer(cursor, data):
    query = """
    INSERT INTO comment (answer_id,message,submission_time, edited_count)
    VALUES (%s,%s,%s,%s)
    """
    cursor.execute(query, data)


@database_common.connection_handler
def search_questions(cursor,searched_question):
    query = """
    SELECT DISTINCT * FROM question
    WHERE title ILIKE %(s_q)s OR message ILIKE %(s_q)s 
    """
    cursor.execute(query, {'s_q': f'%{searched_question}%'})
    return cursor.fetchall()

@database_common.connection_handler
def search_answers(cursor, searched_answer):
    query = """
        SELECT DISTINCT question_id FROM answer 
        WHERE  message ILIKE %(s_a)s
        """
    cursor.execute(query, {'s_a': f'%{searched_answer}%'})
    return cursor.fetchall()



@database_common.connection_handler
def update_answer(cursor,id,message):
    query = """
    UPDATE answer
    SET message = %(message)s
    WHERE id = %(id)s"""
    cursor.execute(query, {'id': id, 'message': message})

@database_common.connection_handler
def get_comment(cursor, id):
    query = """
    SELECT * 
    FROM comment
    WHERE id = %(id)s"""
    cursor.execute(query, {'id':id})
    return cursor.fetchall()

@database_common.connection_handler
def update_comment(cursor, comment):
    query = """
    UPDATE comment
    SET message = (%s), submission_time = (%s), edited_count = edited_count + 1
    WHERE id = (%s)"""
    cursor.execute(query, comment)
