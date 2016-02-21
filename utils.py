import time
from config import *


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
    print type(perWeekWeightGain)
    return cal+((500/0.5)*perWeekWeightGain)

def weightLossCal(cal,perWeekWeightLoss):# gives per day less calorie intake
    return cal-((500/0.5)*perWeekWeightLoss)

def ageCal(date):
    # print date
    currentTime=time.localtime(time.time())
    print currentTime[0]-int(date)
    return currentTime[0]-int(date)

def convertToInt(intString):
    try:
        return math.floor(float(intString))
    except:
        return 0


def importAllFoods():
    nonVegKeyWords = ["beef", "chicken", "lamb", "pork", "pig", "mutton", "meat", "flesh",\
        "egg", "prawn", "oyster", "fish", "crab", "sausage", "ox", "salmon", "filet", "turkey",\
        "rabbit", "molusks", "shrimp", "octopus"]

    vegNode = graph.cypher.execute("match (v:veg) return v")
    nonVegNode = graph.cypher.execute("match (nv:nonVeg) return nv")

    if not vegNode and not nonVegNode:
        print "bullbull"
        veg = Node("veg", name="foodCategory")
        nonVeg = Node("nonVeg", name="foodCategory")
        graph.create(veg)
        graph.create(nonVeg)

    for aFact in nutFacts.find():
        foodName = aFact['name'].split(' ')
        occurence = len(list(set(foodName) & set(nonVegKeyWords)))
        foodNode = Node("Food", name="Food")
        foodNode.properties['ndbno'] = str(aFact['ndbno'])
        foodNode.properties['name'] = str(aFact['name'])
        foodNode.properties['totalCalorie'] = convertToInt(aFact['nutrients'][11]["value"])
        foodNode.properties['carbs'] = convertToInt(aFact['nutrients'][2]["value"])
        foodNode.properties['protiens'] = convertToInt(aFact['nutrients'][0]["value"])
        foodNode.properties['fats'] = convertToInt(aFact['nutrients'][1]["value"])

        graph.create(foodNode)
        print str(aFact['name'])

        if occurence > 0:
            graph.cypher.execute(
                "match (nv:nonVeg), (fd:Food {name:'"+str(aFact['name']).replace("'", "")+"'})"+
                " create unique (fd)-[r:is]->(nv) return r"
            )
        else:
            graph.cypher.execute(
                "match (v:veg), (fd:Food {name:'"+str(aFact['name']).replace("'", "")+"'})"+
                " create unique (fd)-[r:is]->(v) return r"
            )
            

def createDietNode(calorieCount, carbs, fats, lipids,
            proteins, dietType, relate):
    dietNode = Node("Dietplan", name="Dietplan")
    dietNode.properties['calorieCount'] = calorieCount
    dietNode.properties['carbs'] = carbs
    dietNode.properties['fats'] = fats
    dietNode.properties['proteins'] = proteins
    dietNode.properties['dietType'] = dietType
    createdDietNode = graph.create(dietNode)


    if relate == 'on':
        makeFoodRelations(createdDietNode._id)
        pass
    return True


def addCaloricValuesToMongo():

    for aFact in nutFacts.find():
        total_calorie = 0
        for nutrient in aFact['nutrients']:
            if nutrient['value'] != '--':
                total_calorie += float(nutrient['value'])
        print aFact['name']
        x = nutFacts.update_one({'name': aFact['name']}, {'$set': {'totalCalorie': total_calorie}})
        print x.raw_result



def query():
    print nutFacts.find_one({"name": "Hamburger"})


def populateMongoDB():

    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            with open(os.path.join(subdir, file)) as fin:
                facts = json.load(fin)
                nutFacts.insert_one(facts)
