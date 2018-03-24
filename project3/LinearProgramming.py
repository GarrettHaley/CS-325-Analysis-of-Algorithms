import pulp
import math
from matplotlib import pyplot as plt
def warmUp():
	LP_Solution = pulp.LpProblem("My LP Solution",pulp.LpMinimize)

	a = pulp.LpVariable('a', lowBound=0, cat='Continuous')
	b = pulp.LpVariable('b', lowBound=0, cat='Continuous')
	M = pulp.LpVariable('M', lowBound=0, cat='Continuous')
	x = [1,2,3,5,7,8,10]
	y = [3,5,7,11,14,15,19]
	LP_Solution += M, "Ex"
	for i in range(len(x)):
		LP_Solution += M >= a*x[i] + b - y[i]
		LP_Solution += M >= -(a*x[i] + b) + y[i]

	LP_Solution.solve()
	print ("First problem")
	for variable in LP_Solution.variables():
   		print "{}={}".format(variable.name, variable.varValue)

def read_file_input(f_name, varType):
	myList = []
	newList = []
	f = open(f_name, 'r')
    	for line in f:
		line = line.rstrip('\n\r')
        	split_line = line.split(';')
        	myList.append(split_line)
	for i in range(len(myList)):
		if varType == 'd':
			newList.append(myList[i][8])
		if varType == 'T':
			newList.append(myList[i][7])
	return newList


def warmingUp():
	LP_Solution = pulp.LpProblem("My LP Solution",pulp.LpMinimize)
	m = pulp.LpVariable('m', None, cat = 'continuous') 
	x0 = pulp.LpVariable('x0', None, cat = 'continuous')
	x1 = pulp.LpVariable('x1',None, cat = 'continuous')	
	x2 = pulp.LpVariable('x2', None,cat = 'continuous')
	x3 = pulp.LpVariable('x3', None, cat = 'continuous')
	x4 = pulp.LpVariable('x4', None, cat = 'continuous')
	x5 = pulp.LpVariable('x5', None, cat = 'continuous')
	D = []
	d = []
	t = []
	T = []
	D = read_file_input("data.txt", 'd')
	t = read_file_input("data.txt", 'T')
	t.remove('average')
	D.remove('day')
	for i in t:
		T.append(float(i))
	for i in D:
		d.append(int(i))	
	
	LP_Solution += m, "Ex"
	for i in range(len(d)):
                LP_Solution += m >= x0 + x1 * d[i] + x2 * math.cos((2*3.14159*d[i])/365.25) + x3 * math.sin((2*3.14159*d[i])/365.25) + x4 * math.cos((2*3.14159*d[i])/(365.25*10.7)) + x5 * math.sin((2*3.14159*d[i])/(365.25*10.7))- T[i]
		LP_Solution += -m <= x0 + x1 * d[i] + x2 * math.cos((2*3.14159*d[i])/365.25) + x3 * math.sin((2*3.14159*d[i])/365.25) + x4 * math.cos((2*3.14159*d[i])/(365.25*10.7)) + x5 * math.sin((2*3.14159*d[i])/(365.25*10.7))- T[i]
        LP_Solution.solve()
	print("second problem")
        for variable in LP_Solution.variables():
                print "{}={}".format(variable.name, variable.varValue)

def main():
	warmUp()
	warmingUp()
main()
