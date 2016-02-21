from py2neo import Graph
# from pymongo import MongoClient
import time
import os
# client=MongoClient()
# db=client["nutrition1"]
# col=db["posts"]
graph=Graph()
tx=graph.cypher.begin()
	

currentTime=time.localtime(time.time())
date=str(currentTime[2])+"/"+str(currentTime[1])+"/"+str(currentTime[0])
personid=raw_input("enter your person id? ")
ques=raw_input("did you follow your diet plan today?(y/n)")
if(ques=='y'):
	print "good"
	# insert the data to redis for the purticular date and purticular meal
elif(ques=='n'):
	cal=float(raw_input("how much calorie?"))
	protienM=float(raw_input("how much Max protiens?"))
	protienMi=float(raw_input("how much Min protiens?"))
	carbsM=float(raw_input("how much Max Carbs? "))
	carbsMi=float(raw_input("how much Min carbs? "))
	fats=float(raw_input("how much fats? "))
	if(currentTime[3]>=20 or currentTime[3]<=4):
		meal="Meal3"
		statement="match(p:person{id:"+personid+"}) create("+meal+":"+meal+"{calorie:"+str(cal)+\
				",protiens:"+str(protienM)+\
				",carbs:"+str(carbsM)+\
				",fats:"+str(fats)+"})  create(p)-[on:on{date:'"+date+"'}]->("+meal+")"
	elif(currentTime[3]>=4 and currentTime[3]<=11):
		meal="Meal1"
		statement="match(p:person{id:"+str(personid)+"})-[:follows]->(neighbors)"\
		"return neighbors.calorie AS calorie,neighbors.ProtienMax AS ProtienMax"\
		",neighbors.ProtienMin AS ProtienMin, neighbors.CarbMax AS CarbMax"\
		",neighbors.CarbMin AS CarbMin,neighbors.FatReq AS FatReq"
		p=graph.cypher.execute(statement)
		calorieLeft=p[0].calorie-cal
		ProtienMinLeft=p[0].ProtienMin-protienMi
		ProtienMaxLeft=p[0].ProtienMax-protienM
		CarbMaxLeft=p[0].CarbMax-carbsM
		CarbMinLeft=p[0].CarbMin-carbsMi
		FatReqLeft=p[0].FatReq-fats
		statement="match(p:person{id:"+personid+"}) create("+meal+":"+meal+"{time:'4-11',cal:"+str(cal)+\
				",ProtienMax:"+str(protienM)+",ProtienMin:"+str(protienMi)+\
				",CarbMax:"+str(carbsM)+\
				",CarbMin:"+str(carbsMi)+\
				",FatReq:"+str(fats)+\
				"})"\
				" create(Meal2:Meal2{time:'11-17',cal:"+str(calorieLeft/2)+\
				",ProtienMax:"+str(ProtienMaxLeft/2)+",ProtienMin:"+str(ProtienMinLeft/2)+\
				",CarbMax:"+str(CarbMaxLeft/2)+\
				",CarbMin:"+str(CarbMinLeft/2)+\
				",FatReq:"+str(FatReqLeft/3)+\
				"})"\
				" create(Meal3:Meal3{time:'17-4',cal:"+str(calorieLeft/2)+\
				",ProtienMax:"+str(ProtienMaxLeft/2)+",ProtienMin:"+str(ProtienMinLeft/2)+\
				",CarbMax:"+str(CarbMaxLeft/2)+\
				",CarbMin:"+str(CarbMinLeft/2)+\
				",FatReq:"+str(FatReqLeft/3)+\
				"})"\
				" create(p)-[on:on{date:'"+date+"'}]->("+meal+")"\
				" create("+meal+")-[new:new]->(Meal2)"\
				" create(Meal2)-[:new]->(Meal3)"

	elif(currentTime[3]>=11 and currentTime[3]<=20):
		meal="Meal2"
		statement="match(p:person{id:"+str(personid)+"})-[:follows]->(neighbors)"\
		"return neighbors.calorie AS calorie,neighbors.ProtienMax AS ProtienMax"\
		",neighbors.ProtienMin AS ProtienMin, neighbors.CarbMax AS CarbMax"\
		",neighbors.CarbMin AS CarbMin,neighbors.FatReq AS FatReq"
		p=graph.cypher.execute(statement)
		calorieLeft=p[0].calorie-(p[0].calorie/3)-cal
		ProtienMinLeft=p[0].ProtienMin-(p[0].ProtienMin/3)-protienMi
		ProtienMaxLeft=p[0].ProtienMax-(p[0].ProtienMax/3)-protienM
		CarbMaxLeft=p[0].CarbMax-(p[0].CarbMax/3)-carbsM
		CarbMinLeft=p[0].CarbMin-(p[0].CarbMin/3)-carbsMi
		FatReqLeft=p[0].FatReq-(p[0].FatReq/3)-fats
		statement="match(p:person{id:"+personid+"}) create("+meal+":"+meal+"{time:'4-11',cal:"+str(cal)+\
				",ProtienMax:"+str(protienM)+",ProtienMin:"+str(protienMi)+\
				",CarbMax:"+str(carbsM)+\
				",CarbMin:"+str(carbsMi)+\
				",FatReq:"+str(fats)+\
				"})"\
				" create(Meal2:Meal2{time:'11-17',cal:"+str(calorieLeft)+\
				",ProtienMax:"+str(ProtienMax)+",ProtienMin:"+str(ProtienMin)+\
				",CarbMax:"+str(CarbMaxLeft)+\
				",CarbMin:"+str(CarbMinLeft)+\
				",FatReq:"+str(FatReqLeft)+\
				"})"\
				" create(p)-[on:on{date:'"+date+"'}]->("+meal+")"\
				" create("+meal+")-[new:new]->(Meal3)"
				
	print statement
	tx.append(statement)
	tx.commit()	

