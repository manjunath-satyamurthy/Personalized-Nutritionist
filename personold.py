import redis
import time
from py2neo import Graph, Node, Relationship, authenticate

authenticate("localhost:7474", "neo4j", "Abcdef1234")
graph=Graph()
tx=graph.cypher.begin()
r=redis.StrictRedis(host="localhost",port="6379",db=0)
s=r.keys("*.userDetails.*")
userId=0

for x in s:
	if userId<int(x[0]):
		userId=int(x[0])


def calorie(height,weight,age,gender,activity_lvl):
	if(gender=='M'):
		BEE=66.5+(13.8*(weight))+(5.0*(height))-(6.8*(age))
		calorie_intake=activity_lvl*BEE
		return calorie_intake
	elif(gender=='F'):
		BEE = 655.1 + (9.6*(weight))+(1.9*(height))-(4.7*(age))
		calorie_intake=activity_lvl*BEE
		return calorie_intake

def protienMin(weight):
	return weight*(.8)
def protienMax(weight):
	return weight*(1.0)
def carbMin(cal):
	return ((cal*(.45))/4)
def carbMax(cal):
	return ((cal*(.6))/4)
def fatReq(cal):
	return ((cal*(.3))/9)
def weightGainCal(cal,perWeekWeightGain):#gives per day extra calorie intake
	return cal+((500/0.5)*perWeekWeightGain)
def weightLossCal(cal,perWeekWeightLoss):# gives per day less calorie intake
	return cal-((500/0.5)*perWeekWeightLoss)
def ageCal(date):
	currentTime=time.localtime(time.time())
	return currentTime[0]-int(date)

for x in range(1,(userId+1)):
	name=r.get(str(x)+".userDetails.name").split(",")[0].replace('"',"")
	height=float(r.get(str(x)+".userDetails.height").split(",")[0].replace('"',""))
	weight=float(r.get(r.keys(str(x)+".userWeight.*")[0]).split(",")[0])
	date=r.get(str(x)+".userDetails.birthdate").split(",")[0].replace('"',"").split('.')[2]
	gender=r.get(str(x)+".userDetails.gender").split(",")[0].replace('"',"")
	goal=r.get(str(x)+".userGoal").split(",")[0].replace('"',"")
	age=ageCal(date)
	lvl=raw_input("wass ist ihr activity level? \n1. sedentary \n2. Lightly active \n3. Moderately active \n4. very active \n5. extra active\n")
	if(lvl=='1'):
		activity=1.2
	elif(lvl=='2'):
		activity=1.375
	elif(lvl=='3'):
		activity=1.55
	elif(lvl=='4'):
		activity=1.725
	elif(lvl=='5'):
		activity=1.9
	else:
		print "wrong input"
		activity=1.2
	print gender
	calorieIntake=calorie(height,weight,float(age),gender,activity)
	protienM=protienMax(weight)
	protienMi=protienMin(weight)
	print calorieIntake
	
	if(goal=='weightLoss'):
		perWeekWeightLoss=float(raw_input("how much weight loss per week? we recommend not more than 1 kg/week"))
		calReq=weightLossCal(calorieIntake,perWeekWeightLoss)
		carbM=carbMax(calReq)
		carbMi=carbMin(calReq)
		fatR=fatReq(calReq)
		statement="create(person:person{name:'"+name+"',id:"+str(x)+\
		",height:"+str(height)+\
		",weight:"+str(weight)+\
		",age:"+str(age)+\
		",gender:'"+str(gender)+\
		"',activity:"+str(activity)+"}),(dietPlan:dietPlan{type:'"+goal+"',calorie:"+str(calReq)+\
		",ProtienMax:"+str(protienM)+\
		",ProtienMin:"+str(protienMi)+\
		",CarbMax:"+str(carbM)+\
		",CarbMin:"+str(carbMi)+\
		",FatReq:"+str(fatR)+\
		"}),(Meal1:Meal1{time:'4-11',cal:"+str(calReq/3)+\
		",ProtienMax:"+str(protienM/3)+",ProtienMin:"+str(protienMi/3)+\
		",CarbMax:"+str(carbM/3)+\
		",CarbMin:"+str(carbMi/3)+\
		",FatReq:"+str(fatR/3)+\
		"}),(Meal2:Meal2{time:'11-17',cal:"+str(calReq/3)+\
		",ProtienMax:"+str(protienM/3)+",ProtienMin:"+str(protienMi/3)+\
		",CarbMax:"+str(carbM/3)+\
		",CarbMin:"+str(carbMi/3)+\
		",FatReq:"+str(fatR/3)+\
		"}),(Meal3:Meal3{time:'17-4',cal:"+str(calReq/3)+\
		",ProtienMax:"+str(protienM/3)+",ProtienMin:"+str(protienMi/3)+\
		",CarbMax:"+str(carbM/3)+\
		",CarbMin:"+str(carbMi/3)+\
		",FatReq:"+str(fatR/3)+"}),(person)-[follows:follows]->(dietPlan),(dietPlan)-[has:has]->(Meal1),(dietPlan)-[:has]->(Meal2),(dietPlan)-[:has]->(Meal3)"

	elif(goal=='maintainWeight'):
		carbM=carbMax(calorieIntake)
		carbMi=carbMin(calorieIntake)
		fatR=fatReq(calorieIntake)
		statement="create(person:person{name:'"+name+"',id:"+str(x)+\
		",height:"+str(height)+\
		",weight:"+str(weight)+\
		",age:"+str(age)+\
		",gender:'"+str(gender)+\
		"',activity:"+str(activity)+"}),(dietPlan:dietPlan{type:'"+goal+"',calorie:"+str(calorieIntake)+\
		",ProtienMax:"+str(protienM)+\
		",ProtienMin:"+str(protienMi)+\
		",CarbMax:"+str(carbM)+\
		",CarbMin:"+str(carbMi)+\
		",FatReq:"+str(fatR)+\
		"}),(Meal1:Meal1{time:'4-11',cal:"+str(calorieIntake/3)+\
		",ProtienMax:"+str(protienM/3)+",ProtienMin:"+str(protienMi/3)+\
		",CarbMax:"+str(carbM/3)+\
		",CarbMin:"+str(carbMi/3)+\
		",FatReq:"+str(fatR/3)+\
		"}),(Meal2:Meal2{time:'11-17',cal:"+str(calorieIntake/3)+\
		",ProtienMax:"+str(protienM/3)+",ProtienMin:"+str(protienMi/3)+\
		",CarbMax:"+str(carbM/3)+\
		",CarbMin:"+str(carbMi/3)+\
		",FatReq:"+str(fatR/3)+\
		"}),(Meal3:Meal3{time:'17-4',cal:"+str(calorieIntake/3)+\
		",ProtienMax:"+str(protienM/3)+",ProtienMin:"+str(protienMi/3)+\
		",CarbMax:"+str(carbM/3)+\
		",CarbMin:"+str(carbMi/3)+\
		",FatReq:"+str(fatR/3)+"}),(person)-[follows:follows]->(dietPlan),(dietPlan)-[has:has]->(Meal1),(dietPlan)-[:has]->(Meal2),(dietPlan)-[:has]->(Meal3)"

	elif(goal=='massGain'):
		perWeekWeightGain=float(raw_input("how much weight gain per week? we recommend not more than 1 kg/week"))
		calReq=weightGainCal(calorieIntake,perWeekWeightGain)
		carbM=carbMax(calReq)
		carbMi=carbMin(calReq)
		fatR=fatReq(calReq)
		statement="create(person:person{name:'"+name+"',id:"+str(x)+\
		",height:"+str(height)+\
		",weight:"+str(weight)+\
		",age:"+str(age)+\
		",gender:'"+str(gender)+\
		"',activity:"+str(activity)+"}),(dietPlan:dietPlan{type:'"+goal+"',calorie:"+str(calReq)+\
		",ProtienMax:"+str(protienM)+\
		",ProtienMin:"+str(protienMi)+\
		",CarbMax:"+str(carbM)+\
		",CarbMin:"+str(carbMi)+\
		",FatReq:"+str(fatR)+\
		"}),(Meal1:Meal1{time:'4-11',cal:"+str(calReq/3)+\
		",ProtienMax:"+str(protienM/3)+",ProtienMin:"+str(protienMi/3)+\
		",CarbMax:"+str(carbM/3)+\
		",CarbMin:"+str(carbMi/3)+\
		",FatReq:"+str(fatR/3)+\
		"}),(Meal2:Meal2{time:'11-17',cal:"+str(calReq/3)+\
		",ProtienMax:"+str(protienM/3)+",ProtienMin:"+str(protienMi/3)+\
		",CarbMax:"+str(carbM/3)+\
		",CarbMin:"+str(carbMi/3)+\
		",FatReq:"+str(fatR/3)+\
		"}),(Meal3:Meal3{time:'17-4',cal:"+str(calReq/3)+\
		",ProtienMax:"+str(protienM/3)+",ProtienMin:"+str(protienMi/3)+\
		",CarbMax:"+str(carbM/3)+\
		",CarbMin:"+str(carbMi/3)+\
		",FatReq:"+str(fatR/3)+"}),(person)-[follows:follows]->(dietPlan),(dietPlan)-[has:has]->(Meal1),(dietPlan)-[:has]->(Meal2),(dietPlan)-[:has]->(Meal3)"

	print statement
	tx.append(statement)
	

tx.commit()


