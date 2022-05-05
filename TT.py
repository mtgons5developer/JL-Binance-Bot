import re
string1 = "(0,)"
pattern = re.compile('\W')
string1 = re.sub(pattern, '', string1)
print(string1)


# import sqlparse

# queries = '''
# CREATE TABLE foo (id INTEGER);
# CREATE TABLE bar (id INTEGER, name VARCHAR);
# SELECT foo FROM bar WHERE id IN (1,2,3);
# DELETE FROM bar WHERE id IN (3, 4);
# -- a comment
# DELETE FROM bar WHERE name IN ('chaos','atlas');
# '''

# for i, stmt, in enumerate(sqlparse.split(queries)):
#     sql = stmt.strip()
#     if not sql:
#         continue
#     print(i, sql)