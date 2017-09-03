from models import Teacher

import csv

with open('teachers.csv', 'r') as f:
	reader = csv.reader(f)
	for row in reader:
		_, created = Teacher.objects.get_or_create(
			id = int(row[0]),
			tName = row[1],
			tEmail = row[2],
			tCafedra = int(row[3]),
			tDegree = row[4],
			tTitle = row[5]
		)