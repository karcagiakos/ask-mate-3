import database_common
from psycopg2 import sql
from markupsafe import Markup


def markup(searched_question,details):
    for dicts in details:
        for key, value in dicts.items():
            if key == 'title' or key == 'message':
                value = value.split()
                new = []
                for i in range(len(value)):
                    if searched_question.lower() == value[i].lower():
                        new.append(f'<mark>{searched_question}</mark>')
                    else:
                        new.append(value[i])
                dicts[key] = Markup(" ".join(new))
    return details


@database_common.connection_handler
def get_questions(cursor):
    query = """
    SELECT * FROM question ORDER BY submission_time DESC
    """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def last_five_questions(cursor, order_by):
    cursor.execute(sql.SQL("SELECT * FROM question ORDER BY {order_by} LIMIT 5").
           format(order_by=sql.Identifier(order_by)))
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
    ORDER BY vote_number DESC
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
        SELECT * FROM answer 
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


@database_common.connection_handler
def get_all_the_comments(cursor):
    query ='''
    SELECT *
    FROM comment ORDER BY submission_time'''
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def sort_questions(cursor, order_by):
    cursor.execute(sql.SQL("SELECT * FROM question ORDER BY {order_by}").
                              format(order_by=sql.Identifier(order_by)))
                                    # sort=sql.Literal(sort)))
    return cursor.fetchall()


@database_common.connection_handler
def get_tag(cursor):
    query = """
    SELECT *
    FROM tag"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def add_tag(cursor, tag):
    query = """
    INSERT INTO tag (name)
    VALUES (%(tag)s) ON CONFLICT DO NOTHING"""
    cursor.execute(query, {'tag':tag})


@database_common.connection_handler
def delete_tag(cursor, tag):
    pass


@database_common.connection_handler
def add_tag_question(cursor, data):
    query = """
    INSERT INTO question_tag (question_id, tag_id)
    VALUES (%s, %s) ON CONFLICT DO NOTHING"""
    cursor.execute(query, data)


@database_common.connection_handler
def get_question_id_with_tag_name(cursor, question_id):
    query = '''SELECT tag.name,tag.id,question_tag.question_id
    FROM question
    JOIN question_tag
    ON question.id = question_tag.question_id
    JOIN tag
    ON tag.id = question_tag.tag_id
    WHERE question_id = %(q_i)s'''
    cursor.execute(query, {'q_i': question_id})
    return cursor.fetchall()


@database_common.connection_handler
def delete_tag_from_question(cursor, ids):
    query = """
    DELETE FROM question_tag
    WHERE question_id = (%s) AND tag_id = (%s)"""
    cursor.execute(query, ids)