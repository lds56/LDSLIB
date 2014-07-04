import mysql.connector
from django.shortcuts import render_to_response

def book_list(query):
	cnx = mysql.connector.connect(user='root', 
			      password='19941018',
                              host='127.0.0.1',
                              database='test')
	cursor = cnx.cursor()
	query = ("SELECT * FROM A "
		"WHERE gentle = %s")
	cursor.execute(query, ("M"))
	#for (no, name, gentle) in cursor:
	#	print("{} | {} | {}:".format(no, name, gentle))
	lists = [row[0] for row in cursor.fetchall()]
	#print lists
	return render_to_response('book_list.html', {'list': lists})
	cursor.close()
	cnx.close()

