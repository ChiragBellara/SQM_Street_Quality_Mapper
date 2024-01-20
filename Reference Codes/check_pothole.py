import csv
import statistics
from array import *
count = 0

data_Arr = []
avg_pothole = []
	
with open("feeds.csv") as log:
	total = 0
	output = []
	read_logs = csv.DictReader(log,delimiter=',',quotechar='|')
	i=1
	j=0
	for row in read_logs:
		if row['field3'] == 'z':
			continue
		total+=float(row['field3'])
		timestamp = str(row['created_at'])
		acc = float(row['field3'])
		output.append(float(row['field3']))
		data_Arr.insert(i,[timestamp,acc])
		count+=1
		i+=1
	avg = total/count
	sdev = statistics.stdev(output)
	#print(sdev)
	#print(data_Arr)
	for item in data_Arr:
		timestamp = item[0]
		new_tstmp = timestamp.split(' ')
		timestamp = new_tstmp[1].strip(':')
		acc_z = item[1]
		diff = avg - float(acc_z)
		#print(diff)
		diff = abs(diff)
		if diff > 2:
			if j==0:
				avg_pothole.insert(j,[timestamp,diff])
				print(str(timestamp)+' , '+str(diff)+" :Pothole Detected")
			else:
				difference_tstmp = float(timestamp) - float(data_Arr[j-1][0])
				if difference_tstmp > 100:
					avg_pothole.insert(j,[timestamp,diff])
					print(str(timestamp)+' , '+str(diff)+" :Pothole Detected")
			j+=1
			if diff>=2 and diff<=4:
				print("Medium")
			else:
				print("High")
			#print(str(timestamp)+' , '+str(diff))
