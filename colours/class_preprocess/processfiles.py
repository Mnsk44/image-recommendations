import csv
import pickle
# Prosessoi omaluokittelu.csv tiedoston noukkimalla mukaan vain ne rivit joita on tehty kutistettut kuvat lista.txt
#

f = open('lista.txt', 'r')
kuvat = f.read().splitlines()
f.close()

with open('omaluokittelu.csv', 'r') as f:
  reader = csv.reader(f)
  omaluokittelu = list(reader)
f.close()

omaluokittelu2 = []
for i in omaluokittelu:
    if i[0] in kuvat:                
        omaluokittelu2.append([i[0], i[1], i[2]])  


with open('omaluokittelu.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    for i in omaluokittelu2:
        writer.writerow(i)

csvfile.close()