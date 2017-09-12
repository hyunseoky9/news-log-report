# Log Report
this project creates a printed text using python db-api based on the log database of 
news website, and the author and article data as well. The report answers 3 posed questions
about meta data of the website traffic:

1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

## How to Run the Script
First you need the database which can be requested by enrolling in Udacity's 
full stack web developer nanodegree program. Once you get the ```newsdata.zip``` file,
you need to download vagrantup and virtual machine, and place ```newsdata.sql``` in the vagrant folder in [Udacity's repo](https://github.com/udacity/fullstack-nanodegree-vm). Then, install vagrantup by typing ```vagrant up``` in the command line, and then ```vagrant ssh``` to connect to the virtual machine.
Once you are connected to the VM, type ```cd /vagrant``` and type ```psql -d news -f newsdata.sql```, which will create the 3 tables (log, authors, articles) needed for getting the report.

Once the tables are created, go into the database (```psql news```) and type in the following.

```
create view q1 as
	select substring(path,10,100), count(*) as views
	from log
	where status='200 OK' and path like '/article/%' group by path order by views desc;
```
and
```
alter table articles add path text;
update articles set path='/article/candidate-is-jerk' where title='Candidate is jerk, alleges rival'
update articles set path='/article/bears-love-berries' where title='Bears love berries, alleges bear'
update articles set path='/article/bad-things-gone' where title='Bad things gone, say good people'
update articles set path='/article/media-obsessed-with-bears' where title='Media obsessed with bears'
update articles set path='/article/trouble-for-troubled' where title='Trouble for troubled troublemakers'
update articles set path='/article/so-many-bears' where title='There are a lot of bears'
update articles set path='/article/balloon-goons-doomed' where title='Balloon goons doomed'
update articles set path='/article/goats-eat-googles' where title like 'Goats%'
```