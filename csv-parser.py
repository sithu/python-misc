import csv

def read(infile='input.csv',outfile='output.csv'):
   reader = csv.reader(open(infile, 'rb'))
   writer = csv.writer(open(outfile, 'wb'))
   
   for row in reader:
      if row:
         sid = row[0]
         sid = sid[2:]
         print "'%s': 0," % sid
         writer.writerow(sid)
   
   
read("all-students.csv")