
from book_yz.db.models import *
from book_yz.sync_mysql_pipelines import session

num = session.query(Books.book_num).all()
c = 1
for i in num:
    if len(i[0])>12:
        print(i[0])
        c +=1
print(c)
"9787519020613","9787519015022","9787519015107","9787519018351"