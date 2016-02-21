from config import *
from utils import *
from cypherQueries import *

from flask import redirect
from flask import jsonify


@app.route('/likeFood', methods=['POST'])
def likeFood():
    foodName = request.json["foodName"]
    userId = session.get("userId")
    like = graph.cypher.execute(
        "match (p: person), (f:Food) where p.id='"+str(userId)+
        "' and f.name ='"+foodName+"' create unique (p)-[r:likes]->(f) return r"
        )

    return jsonify(result="Liked Food Successfully",
                   status="success")


@app.route('/dashboard', methods=['GET', 'POST'])
def dashbaord():
    if request.method=='GET':
        userId = session.get("userId")
        print userId        
        username = redisConn.get(userId+".userDetails.name").split(",")[0]
        dietPlan = graph.cypher.execute(
            "match (p: person)-[r:follows]->(d:dietPlan) where p.name='"+username+"' return d"
            )

        foods = graph.cypher.execute(
            "match (p: person)-[*0..3]->(f:Food) where p.name='"+
            username+"' return f"
            )

        likedFoods = getLikedFoods(userId)
        suggestedFoods = getFoodBasedOnLikes(userId)
        allFoods = getAllFoods()

        meals = []
        temp = []

        for food in foods:
            if len(temp) < 3:
                temp.append(str(food[0]["name"]))
            else:
                meals.append(temp)
                temp = []

        context = {
            "username": username,
            "calorie": dietPlan[0][0]['calorie'],
            "carbsMin": dietPlan[0][0]['CarbMin'],
            "carbsMax": dietPlan[0][0]['CarbMax'],
            "protiensMin": dietPlan[0][0]['ProtienMin'],
            "protiensMax": dietPlan[0][0]['ProtienMax'],
            "fats": dietPlan[0][0]['FatReq'],
            "meals": meals,
            "likedFoods": likedFoods,
            "suggestedFoods": suggestedFoods,
            "foods": allFoods
        }
        
        return render_template('dashboard.html', **context)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')

    if request.method == 'POST':
        userId, userName = request.form['userId'], request.form['userName']
        height, weight = request.form['height'], request.form['weight']
        date, goalKg= request.form['dob'], request.form['goalKg']
        gender, foodPrefer = request.form['gender'], request.form['category']
        activityLevel, goal = request.form['activity'], request.form['goal']

        userDetails = [userId, userName, height, weight, date, goalKg, gender, \
            foodPrefer, activityLevel, goal]

        isExisting = isSimilarPersonExisting(*userDetails)
        person = createPerson(*userDetails)
        if not isExisting:
            print "no here"
            dietPlan = createDietPlanForUser(person)
            makeFoodRelations(dietPlan[0][0]._id)
        else:
            # relatePersontoDiet(person, isExisting)
            print "here"
            pass
        session["userId"] = userId
        return redirect('/dashboard')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        userId = request.form['userId']
        keys = redisConn.keys(userId+"*")
        if keys:
            session["userId"] = userId
            return redirect('/dashboard')
        else:
            return "Unauthorized"


@app.route('/createDiet', methods=['GET', 'POST'])
def createDiet():
    if request.method == 'GET':
        return render_template('createDiet.html')

    if request.method == 'POST':
        calorieCount = request.form['calorieCount']
        carbs = request.form['carbs']
        fats = request.form['fats']
        lipids = request.form['lipids']
        proteins = request.form['proteins']
        dietType = request.form['type']
        relate = request.form['relate']
        dietNode = createDietNode(calorieCount, carbs, fats, lipids,
            proteins, dietType, relate)

        if dietNode:
            return "done"
        return "Unsuccessful"

if __name__ == '__main__':
    app.debug = True
    app.run()
