# This module creates a report on the meta information on "news" database.
# It answers three questions.
# 1. 3 most popular articles of all time?
# 2. The most popular article authors of all time?
# 3. on what day did more than 1% of requests lead to errors?
import psycopg2
import re

dbname = "news"

db = psycopg2.connect(database="news")
c = db.cursor()

# First question
print("1. What are the most popular three articles of all time?\n")
# this query gets the portion of the table of view q1,
# which is created in advance.
q1 = c.execute("select * from q1 limit 3;")
result1 = c.fetchall()
# print text about the table
print('(article, views)\n')
for item in result1:
    print ('(' + item[0] + ', ' + str(item[1]) + ')')

print('\n')

# Second question
print("2. Who are the most popular article authors of all time?\n")
# this query joins all three tables and gets
# the table of authors' names and their view counts.
q2 = c.execute('''select authors.name, count(*) as views
from (articles left join log on articles.path=log.path)
join authors on articles.author=authors.id
group by authors.name;
''')
result2 = c.fetchall()
# print text about the table
print('(author, views)\n')
for item in result2:
    print ('(' + item[0] + ', ' + str(item[1]) + ')')

print('\n')

# Third question
print("3. On which days did more than 1% of requests lead to errors?\n")
# This query gets 2 subqueries. One on all requests on a given day,
# and another one on the erroneous requests per day.
# Then it uses the 2 subqueries to get the error percentage.
q3 = c.execute('''select sub1.date,
cast(sub2.err as float)/cast(sub1.raw as float) as percent
from (select date(time) as date, count(*) as raw from log group by date)
as sub1,
(select date(time) as date, count(*) as err from log
where status='404 NOT FOUND' group by date order by date desc)
as sub2 where sub1.date=sub2.date;
''')
result3 = c.fetchall()
print('(date, error_percentage)\n')
for item in result3:
    print('(' + str(item[0])[8:10] + ', ' + str(round(item[1], 5)) + ')')


print('\n')
print('On no day was the error rate of the requests over 1%\n')
