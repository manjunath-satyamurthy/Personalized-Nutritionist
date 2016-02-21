from config import *
from utils import *

def getLikedFoods(userId):
    return graph.cypher.execute(
        "match (p: person)-[r:likes]->(f) where p.id='"+userId+"' return f"
        )

def getFoodBasedOnLikes(userId): 
    return graph.cypher.execute(
        "match (p:person)-[r:likes*2..3]-(f:Food) where p.id='"+userId+"' return f"
        )

def getAllFoods():
    return graph.cypher.execute(
        "match (f:Food) return f"
        )

def isSimilarPersonExisting(userId, userName, height, weight, date, \
    goalKg, gender, foodPrefer, activityLevel, goal):

    diet = graph.cypher.execute(
        "match(p:person)-[:follows]->(d:dietPlan) where d.type CONTAINS '"+
        goal+"'and p.height="+height+" and p.weight="+
        weight+" and p.age="+str(ageCal(date.split("/")[0]))+" and p.gender='"+
        gender+"' return d")

    if diet:
        return True
    else:
        return diet


def makeFoodRelations(dietNodeId):
    print "called"

    meals = graph.cypher.execute(
        "match (d:dietPlan)-[r:has]-(m) where id(d)="+str(dietNodeId)+" return m"
        )

    minCarbs = int(meals[0][0]['CarbMin'])
    maxCarbs = int(meals[0][0]['CarbMax'])
    minProtiens = int(meals[0][0]['ProtienMin'])
    maxProtiens = int(meals[0][0]['ProtienMax'])
    fatReq = int(meals[0][0]['FatReq'])
    calReq = int(meals[0][0]['cal'])
    query = "match (fd: Food) where (fd.totalCalorie >"+str(300)+" and "+\
        "fd.totalCalorie < "+str(calReq+50)+") and (fd.carbs"+\
        " < "+str(maxCarbs+2)+") and (fd.fats < "+str(fatReq+2)+\
        ") and (fd.protiens < "+str(maxProtiens+2)+\
        ") return fd"
    foods = graph.cypher.execute(query)
    print foods
    print query

    meal1, meal2, meal3 = [], [], []

    for food in foods:
        if len(meal1) == len(meal2) == len(meal3):
            meal1.append(food)
        elif len(meal2) < len(meal1):
            meal2.append(food)
        elif len(meal3) < len(meal2):
            meal3.append(food)

        x = graph.cypher.execute(
            "match (m), (f: Food) where id(m)= "+str(meals[0][0]._id)+
            " and id(f)="+str(food[0]._id)+" "+
            "create (m)-[r:canHave]->(f) return r"
            )
        print x

        x = graph.cypher.execute(
            "match (m), (f: Food) where id(m)= "+str(meals[2][0]._id)+
            " and id(f)="+str(food[0]._id)+" "+
            "create (m)-[r:canHave]->(f) return r"
            )
        print x

        x = graph.cypher.execute(
            "match (m), (f: Food) where id(m)= "+str(meals[1][0]._id)+
            " and id(f)="+str(food[0]._id)+" "+
            "create (m)-[r:canHave]->(f) return r"
            )
        print x


def createDietPlanForUser(person):
    _id, goal= person[0]['id'] , person[0]['goal']
    maxProtien = protienMax(person[0]['weight'])
    minProtien = protienMin(person[0]['weight'])

    calorieIntake = calorie(person[0]['height'],
        person[0]['weight'],person[0]['age'],
        person[0]['gender'],person[0]['activity'])
    if goal == "weightLoss":
        calReq=weightLossCal(calorieIntake, person[0]['goalKg'])
    elif goal == "maintainWeight":
        calReq = calorieIntake
    else:
        calReq = weightGainCal(calorieIntake, person[0]['goalKg'])

    minCarb, maxCarb = carbMin(calReq), carbMax(calReq)
    reqFat = fatReq(calReq)

    x = "match (p:person) where p.id='"+_id+\
        "' create (d:dietPlan {name : 'DietPlan', type:'"+goal+\
        "' ,calorie:"+str(calReq)+",ProtienMax:"+\
        str(maxProtien)+",ProtienMin:"+str(minProtien)+\
        ",CarbMax:"+str(maxCarb)+",CarbMin:"+str(minCarb)+\
        ",FatReq:"+str(reqFat)+"}),(m1:Meal1 {name : 'Breakfast', type:'breakfast',cal:"+str(calReq/3)+\
        ",ProtienMax:"+str(maxProtien/3)+",ProtienMin:"+str(minProtien/3)+\
        ",CarbMax:"+str(maxCarb/3)+",CarbMin:"+str(minCarb/3)+\
        ",FatReq:"+str(reqFat/3)+"}),(m2:Meal2 {name : 'Lunch', type:'lunch',cal:"+str(calReq/3)+\
        ",ProtienMax:"+str(maxProtien/3)+",ProtienMin:"+str(minProtien/3)+\
        ",CarbMax:"+str(maxCarb/3)+",CarbMin:"+str(minCarb/3)+\
        ",FatReq:"+str(reqFat/3)+"}),(m3:Meal3 {name : 'Dinner', type:'dinner',cal:"+str(calReq/3)+\
        ",ProtienMax:"+str(maxProtien/3)+",ProtienMin:"+str(minProtien/3)+\
        ",CarbMax:"+str(maxCarb/3)+",CarbMin:"+str(minCarb/3)+",FatReq:"+str(reqFat/3)+\
        "}),(p)-[:follows]->(d),(d)-[:has]->(m1),(d)-[:has]->(m2),(d)-[:has]->(m3) return d"

    return graph.cypher.execute(x)



def createPerson(userId, userName, height, weight, \
    date, goalKg, gender, foodPrefer, activityLevel, goal):
    redisConn.set(userId+".userDetails.name", userName)
    redisConn.set(userId+".userDetails.height", height)
    redisConn.set(userId+".userDetails.weight", weight)
    redisConn.set(userId+".userDetails.birthdate", ".".join(date.split("/")))
    redisConn.set(userId+".userDetails.gender", goal+",")
    redisConn.set(userId+".userDetails.activity", activityLevel)
    redisConn.set(userId+".userDetails.goalKg", goalKg)
    redisConn.set(userId+".userGoal", goal)

    age = ageCal(date.split("/")[2])

    person = Node("person")
    person.properties['name'] = userName
    person.properties['id'] = userId
    person.properties['height'] = int(height)
    person.properties['weight'] = int(weight)
    person.properties['age'] = int(age)
    person.properties['gender'] = gender
    person.properties['goal'] = goal
    person.properties['goalKg'] = float(goalKg)
    person.properties['activity'] = float(activityLevel)
    return graph.create(person)
