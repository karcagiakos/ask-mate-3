import database_common
from psycopg2 import sql
from markupsafe import Markup
import bcrypt


def hash_password(plain_text_password):
    # By using bcrypt, the salt is saved into the hash itself
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)


def markup(searched_question, details):
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
def last_five_questions(cursor):
    cursor.execute(sql.SQL("SELECT * FROM question ORDER BY submission_time DESC LIMIT 5").format())
    return cursor.fetchall()


@database_common.connection_handler
def get_answers(cursor):
    query = """
    SELECT * FROM answer ORDER BY submission_time DESC
    """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def list_answers(cursor, q_id):
    query = """
    SELECT * FROM answer 
    WHERE question_id = %(q_id)s
    ORDER BY vote_number DESC
    """
    cursor.execute(query, {'q_id': q_id})
    return cursor.fetchall()


@database_common.connection_handler
def display_answer(cursor, c_id):
    query = """
    SELECT * FROM answer 
    WHERE  id = %(c_id)s
    """
    cursor.execute(query, {'c_id': c_id})
    return cursor.fetchall()


@database_common.connection_handler
def get_single_question(cursor, c_id):
    query = """
    SELECT * FROM question WHERE id = %(c_id)s
    """
    cursor.execute(query, {'c_id': c_id})
    return cursor.fetchall()


@database_common.connection_handler
def add_new_answer(cursor, data):
    query = """
    INSERT INTO answer (submission_time,vote_number, question_id, message, image, state, user_id)
    VALUES (%s,%s,%s,%s,%s,%s,%s)
    """
    cursor.execute(query, data)


@database_common.connection_handler
def add_new_question(cursor, data):
    query = """
    INSERT INTO question (submission_time,view_number, vote_number, title, message, image, user_id)
    VALUES (%s,%s,%s,%s,%s,%s,%s)
    """
    cursor.execute(query, data)


@database_common.connection_handler
def update_question(cursor, data):
    query = """
    UPDATE question
    SET title = %s, message = %s
    WHERE id = %s
    """
    cursor.execute(query, data)


@database_common.connection_handler
def delete_answer(cursor, c_id):
    query = """
     DELETE FROM answer
     WHERE id = %(c_id)s
     """
    cursor.execute(query, {'c_id': c_id})


@database_common.connection_handler
def delete_question(cursor, c_id):
    query = """
    DELETE FROM question
    WHERE id = %(c_id)s
    """
    cursor.execute(query, {'c_id': c_id})


@database_common.connection_handler
def delete_comment(cursor, c_id):
    query = """
    DELETE FROM comment
    WHERE  id = %(c_id)s   """
    cursor.execute(query, {'c_id': c_id})


@database_common.connection_handler
def update_answer_vote(cursor, c_id, amount):
    query = """
    UPDATE answer
    SET vote_number = vote_number + %(amount)s
    WHERE id = %(c_id)s"""
    cursor.execute(query, {'c_id': c_id, 'amount': amount})


@database_common.connection_handler
def update_question_vote(cursor, c_id, amount):
    query = """
    UPDATE question
    SET vote_number = vote_number + %(amount)s
    WHERE id = %(c_id)s"""
    cursor.execute(query, {'c_id': c_id, 'amount': amount})


@database_common.connection_handler
def update_view_number(cursor, c_id):
    query = """
    UPDATE question
    SET view_number = view_number + 1
    WHERE id = %(c_id)s"""
    cursor.execute(query, {'c_id': c_id})


@database_common.connection_handler
def get_comments_for_questions(cursor, q_id):
    query = """
    SELECT message,submission_time, id, edited_count FROM comment WHERE question_id = %(q_id)s
    """
    cursor.execute(query, {'q_id': q_id})
    return cursor.fetchall()


@database_common.connection_handler
def get_comments_for_answers(cursor, a_id):
    query = """
    SELECT message,submission_time, id, edited_count FROM comment WHERE answer_id = %(a_id)s
    """
    cursor.execute(query, {'a_id': a_id})
    return cursor.fetchall()


@database_common.connection_handler
def add_new_comment_question(cursor, data):
    query = """
    INSERT INTO comment (question_id,message,submission_time, edited_count, user_id)
    VALUES (%s,%s,%s,%s,%s)
    """
    cursor.execute(query, data)


@database_common.connection_handler
def add_new_comment_answer(cursor, data):
    query = """
    INSERT INTO comment (answer_id,message,submission_time, edited_count, user_id)
    VALUES (%s,%s,%s,%s,%s)
    """
    cursor.execute(query, data)


@database_common.connection_handler
def search_questions(cursor, searched_question):
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
def update_answer(cursor, c_id, message):
    query = """
    UPDATE answer
    SET message = %(message)s
    WHERE id = %(c_id)s"""
    cursor.execute(query, {'c_id': c_id, 'message': message})


@database_common.connection_handler
def get_comment(cursor, c_id):
    query = """
    SELECT * 
    FROM comment
    WHERE id = %(c_id)s"""
    cursor.execute(query, {'c_id': c_id})
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
    query = '''
    SELECT *
    FROM comment ORDER BY submission_time'''
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def sort_questions(cursor, order_by):
    cursor.execute(sql.SQL("SELECT * FROM question ORDER BY {order_by}").format(order_by=sql.Identifier(order_by)))
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
    cursor.execute(query, {'tag': tag})


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


@database_common.connection_handler
def get_question_id_by_answer_id(cursor, answer_id):
    query = '''
    SELECT question_id FROM answer
    WHERE id = %(a_i)s'''
    cursor.execute(query, {'a_i': answer_id})
    return cursor.fetchall()


@database_common.connection_handler
def get_emails_and_passwords(cursor):
    query = '''
    SELECT email, password_hash FROM users
    '''
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def add_new_user(cursor, data):
    query = '''
    INSERT INTO users (email,password_hash,registration_date,number_of_questions,
    number_of_answers,number_of_comments,reputation)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    '''
    cursor.execute(query, data)


@database_common.connection_handler
def get_password(cursor, email):
    query = '''
    SELECT password_hash FROM users
    WHERE email = %(e_m)s'''
    cursor.execute(query, {'e_m': email})
    return cursor.fetchall()


@database_common.connection_handler
def get_users(cursor):
    query = '''
    SELECT * FROM users'''
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_user_id(cursor, email):
    query = """
    SELECT id FROM users 
    WHERE email = %(e)s"""
    cursor.execute(query, {'e': email})
    return cursor.fetchall()


@database_common.connection_handler
def increase_question_number(cursor, user_id):
    query = """
    UPDATE users
    SET number_of_questions = number_of_questions + 1
    WHERE id = %(u_i)s"""
    cursor.execute(query, {'u_i': user_id})


@database_common.connection_handler
def increase_answer_number(cursor, user_id):
    query = """
    UPDATE users
    SET number_of_answers = number_of_answers + 1
    WHERE id = %(u_i)s"""
    cursor.execute(query, {'u_i': user_id})


@database_common.connection_handler
def increase_comment_number(cursor, user_id):
    query = """
    UPDATE users
    SET number_of_comments = number_of_comments + 1
    WHERE id = %(u_i)s"""
    cursor.execute(query, {'u_i': user_id})


@database_common.connection_handler
def get_user(cursor, user_id):
    query = """
    SELECT * FROM users 
    WHERE id = %(user_id)s"""
    cursor.execute(query, {'user_id': user_id})
    return cursor.fetchall()


@database_common.connection_handler
def get_questions_by_user_id(cursor, user_id):
    query = """
    SELECT * FROM question
     WHERE user_id = %(user_id)s"""
    cursor.execute(query, {'user_id': user_id})
    return cursor.fetchall()


@database_common.connection_handler
def get_answers_by_user_id(cursor, user_id):
    query = """
        SELECT * FROM answer
         WHERE user_id = %(user_id)s"""
    cursor.execute(query, {'user_id': user_id})
    return cursor.fetchall()


@database_common.connection_handler
def get_comments_by_user_id(cursor, user_id):
    query = """
        SELECT * FROM comment
         WHERE user_id = %(user_id)s"""
    cursor.execute(query, {'user_id': user_id})
    return cursor.fetchall()


@database_common.connection_handler
def decrease_question_number(cursor, user_id):
    query = """
    UPDATE users
    SET number_of_questions = number_of_questions - 1
    WHERE id = %(u_i)s"""
    cursor.execute(query, {'u_i': user_id})


@database_common.connection_handler
def decrease_answer_number(cursor, user_id):
    query = """
    UPDATE users
    SET number_of_answers = number_of_answers - 1
    WHERE id = %(u_i)s"""
    cursor.execute(query, {'u_i': user_id})


@database_common.connection_handler
def decrease_comment_number(cursor, user_id):
    query = """
    UPDATE users
    SET number_of_comments = number_of_comments - 1
    WHERE id = %(u_i)s"""
    cursor.execute(query, {'u_i': user_id})


@database_common.connection_handler
def change_state(cursor, answer_id):
    query = """
    UPDATE answer
    SET state = CASE WHEN state = True THEN False else True END 
    WHERE id = %(answer_id)s"""
    cursor.execute(query, {'answer_id': answer_id})


@database_common.connection_handler
def change_reputation(cursor, num, user_id):
    pass
    query = '''
    UPDATE users
    SET reputation = reputation + %(num)s
    WHERE id = %(user_id)s'''
    cursor.execute(query, {'num': num, 'user_id': user_id})


@database_common.connection_handler
def get_tags_with_nums_of_question(cursor):
    query = '''
    SELECT tag.name AS tag, COUNT(question_tag.question_id) AS quantity
    FROM tag
    LEFT JOIN question_tag ON tag.id = question_tag.tag_id
    LEFT JOIN question ON question_tag.question_id = question.id
    GROUP BY tag.name'''
    cursor.execute(query)
    return cursor.fetchall()
