from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DB_PATH = "db/freelancerMgmtDB.db"

# connect the database to the web app - return connection to database
# this function makes connection to the database and then the db object is used to perform queries on it
def get_db_connection():
    c = sqlite3.connect(DB_PATH)
    c.row_factory = sqlite3.Row
    return c

# route() functions - from geeksforgeeks tutorial
@app.route("/")
def index():
    return render_template("index.html") # app landing page rendering

# show existing profiles
@app.route("/profiles")
def profiles():
    c = get_db_connection() # fetch the database connection object 
    profiles = c.execute("SELECT * FROM profiles").fetchall() # sql select query and fetchall() to store the query result
    c.close() # close the connection
    return render_template("profiles.html", profiles=profiles) # template rendering and profiles query result

# add freelancers page - handles http get and post requests to perform add and fetch operation on the page 
@app.route("/add_freelancer", methods=["GET", "POST"])
def add_freelancer():
    if request.method == "POST":
        # get the info from the post request by the user and insert it into the database profiles table
        name = request.form["name"]
        rate = request.form["rate"]
        availability = request.form["availability"]

        c = get_db_connection() # make connection to the database
        c.execute(
            "INSERT INTO profiles (name, rate, availability) VALUES (?, ?, ?)",
            (name, rate, availability),
        ) # execute query
        c.commit()
        c.close()
        return redirect(url_for("profiles")) # redirect to profiles page after adding the database entry 

    return render_template("add_freelancer.html") # add_freelancer template rendering

# All Projects currently available in the system
# projects and organizations table are JOINed for mandatory participation, here projects can not exist without organization's existence or in other words projects can only exist if there are linked with organizations table
# can also add a add_projects feature to this app, currently its not implemented!!!
@app.route("/projects")
def projects():
    c = get_db_connection()
    projects = c.execute(
        "SELECT projects.title, projects.budget, organizations.name as organization "
        "FROM projects JOIN organizations ON projects.organizationID = organizations.organizationID"
    ).fetchall()
    c.close()
    return render_template("projects.html", projects=projects) # template rendering and projects result 

# add project page rendering - handles http request made to add_project
@app.route("/add_project", methods=["GET", "POST"])
def add_project():
    c = get_db_connection()
    #collect the form info
    if request.method == "POST":
        title = request.form["title"]
        budget = request.form["budget"]
        organizationID = request.form["organizationID"]

        # perform the data insertion to the projects table
        c.execute(
            "INSERT INTO projects (title, budget, organizationID) VALUES (?, ?, ?)",
            (title, budget, organizationID),
        )
        c.commit()
        c.close()
        return redirect(url_for("projects")) #redirect to projects

    organizations = c.execute(
        "SELECT organizationID, name FROM organizations"
    ).fetchall()
    c.close()

    return render_template("add_project.html", organizations=organizations)


# freelancers to skills mapping 
# formed by profiles and skills N:N JOIN
@app.route("/skills")
def skills():
    c = get_db_connection()
    skills = c.execute(
        "SELECT profiles.name as freelancer, skills.skillName "
        "FROM freelancerSkills "
        "JOIN profiles ON freelancerSkills.flID = profiles.flID "
        "JOIN skills ON freelancerSkills.skillID = skills.skillID"
    ).fetchall()
    c.close()
    return render_template("skills.html", skills=skills) # template rendering and fetch the skills query result

@app.route("/add_skills", methods=["GET", "POST"])
def add_skills():
    c = get_db_connection()

    if request.method == "POST":

        #collect and insert the data to the table
        flID = request.form["flID"]
        skillID = request.form["skillID"]

        c.execute(
            "INSERT INTO freelancerSkills (flID, skillID) VALUES (?, ?)", (flID, skillID)
        )
        c.commit()
        c.close()

        return redirect(url_for("skills"))

    freelancers = c.execute("SELECT flID, name FROM profiles").fetchall()
    skills = c.execute("SELECT skillID, skillName FROM skills").fetchall()
    c.close()

    return render_template(
        "add_skills.html", freelancers=freelancers, skills=skills
    )

# GET AND POST requests for freelancer to project assignments
@app.route("/assignments", methods=["GET", "POST"])
def assignments():
    c = get_db_connection()
    # Make the freelancer assignments - POST freelancer assignment to the assignments table
    if request.method == "POST":
        flID = request.form["flID"]
        projectID = request.form["projectID"]
        c.execute(
            "INSERT INTO assignments (flID, projectID) VALUES (?, ?)", (flID, projectID)
        )
        c.commit()
        c.close()
        return redirect(url_for("assignments"))

    # Fetch existing assignments - GET freelancer assignments from the assignments table
    freelancers = c.execute("SELECT flID, name FROM profiles").fetchall()
    projects = c.execute("SELECT projectID, title FROM projects").fetchall()

    # profiles and projects JOIN N:N relation
    assignments = c.execute(
        "SELECT profiles.name AS freelancer, projects.title AS project "
        "FROM assignments "
        "JOIN profiles ON assignments.flID = profiles.flID "
        "JOIN projects ON assignments.projectID = projects.projectID"
    ).fetchall()
    c.close()
    return render_template(
        "assignments.html", freelancers=freelancers, projects=projects, assignments=assignments
    )

#
@app.route("/refine")
def refine():
    c = get_db_connection()
    #query to fetch al the freelancer matching the set constraint
    initial_query = c.execute(
        "SELECT name, rate, flID FROM profiles WHERE rate > 50"
    ).fetchall()
    c.close()

    # refine query - of high rate freelancers
    # the following part of the code is inspired from web 
    refined_query = []
    for freelancer in initial_query:
        c = get_db_connection()
        #query
        projects = c.execute(
            "SELECT title FROM projects "
            "JOIN assignments ON assignments.projectID = projects.projectID "
            "WHERE assignments.flID = ?",
            (freelancer["flID"],),
        ).fetchall()
        c.close()
        refined_query.append({"freelancer": freelancer, "projects": projects}) # freelancer to projects assignments added to the refined_query array to be able to get the display

    return render_template("refine.html", refined_query=refined_query)

# work history of each freelancer associated with project they participated or currently are
# workHistoy JOIN to profiles and projects
@app.route("/work_history")
def work_history():
    c = get_db_connection()
    #query
    history = c.execute(
        "SELECT profiles.name AS freelancer, projects.title AS project, workHistory.comments, workHistory.role "
        "FROM workHistory "
        "JOIN profiles ON workHistory.flID = profiles.flID "
        "JOIN projects ON workHistory.projectID = projects.projectID"
    ).fetchall()
    c.close()
    return render_template("work_history.html", history=history)

# reviews of each freelancers based on the projects he worked on
# reviews JOIN with profiles and projects 
@app.route("/reviews")
def reviews():
    c = get_db_connection()
    # query
    reviews = c.execute(
        "SELECT profiles.name AS freelancer, projects.title AS project, reviews.rating "
        "FROM reviews "
        "JOIN profiles ON reviews.flID = profiles.flID "
        "JOIN projects ON reviews.projectID = projects.projectID"
    ).fetchall()
    c.close()
    return render_template("reviews.html", reviews=reviews)


if __name__ == "__main__":
    app.run(debug=True)
