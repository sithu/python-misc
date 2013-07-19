import csv

def read(infile='input.csv',outfile='output.csv'):
   reader = csv.reader(open(infile, 'rb'))
   writer = csv.writer(open(outfile, 'wb'))
   
   for row in reader:
      if row:
         names = row[0]
         for each in names.split():
            row[0] = each
            writer.writerow(row)
   
   
read("input.csv")