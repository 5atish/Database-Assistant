import sqlite3
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
import os

## Connectt to SQlite
connection=sqlite3.connect("employee.db")

### Load GOOGLE API
load_dotenv()
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])


## Function To Load Google Gemini Model and provide queries
def get_gemini_response(question,prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt[0],question])
    return response.text

## Fucntion To retrieve query from the database
def read_sql_query(sql,db):
    conn=sqlite3.connect(db)
    cur=conn.cursor()
    cur.execute(sql)
    rows=cur.fetchall()
    conn.commit()
    conn.close()
    for row in rows:
        print(row)
    return rows


## Define Prompt
prompt=[
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name employee and has the following columns -
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        Designation TEXT NOT NULL,
        Location TEXT NOT NULL,
        Salary REAL NOT NULL,
        Age INTEGER NOT NULL,
        Department TEXT NOT NULL,
        Date_of_Joining TEXT NOT NULL,
        Experience INTEGER NOT NULL,
        Email TEXT NOT NULL
    SECTION \n\nFor example,\nExample 1 - Count the total number of employees?,
    the SQL command will be like this SELECT COUNT(*) FROM employee;
    \nExample 2 - Get the sum of all employee salaries?,
    the SQL command will be something like this SELECT SUM(Salary) FROM employee;
    \nExample 3 - Get employees located in 'New York'?,
    the SQL command will be something like this SELECT Name FROM employee WHERE Location = 'New York';
    \nExample 4 - Find employees with more than 5 years of experience?,
    the SQL command will be something like this SELECT Name FROM employee WHERE Experience > 5;
    \nExample 5 - Find the highest-paid employee in each department?,
    the SQL command will be something like this SELECT Department, Name, MAX(Salary) as HighestSalary FROM employee GROUP BY Department, Name;
    \nExample 6 - List all employees with more than 5 years of experience and a salary greater than 75000?,
    the SQL command will be something like this SELECT Name, Salary, Experience FROM employee WHERE Experience > 5 AND Salary > 75000;
    \nExample 7 - Find employees who joined in the last 2 years?,
    the SQL command will be something like this SELECT Name, Designation, Join_Date FROM employee WHERE Join_Date >= DATE('now', '-2 years');
    also the sql code should not have ``` in beginning or end and sql word in output
    """
]

## Streamlit App

st.set_page_config(page_title="SQL_query")
# st.header("Gemini App To Retrieve Data from SQlite")

# Initialize session state to store history if it doesn't exist
if 'history' not in st.session_state:
    st.session_state.history = []

question=st.text_input("Input: ",key="input")
submit=st.button("Answer")

# if submit is clicked
if submit:
    response=get_gemini_response(question, prompt)
    print(response)
    response=read_sql_query(response,"employee.db")
    # st.subheader("The Answer is")
    for row in response:
        print(row)
        st.text(row)

    # Store question and response in history
    st.session_state.history.append((question, response))

# Display all previous questions and answers as history
if st.session_state.history:
    # st.text("History")
    for i, (q, res) in enumerate(reversed(st.session_state.history[:-1])):
        st.text(f"Question {i+1}: {q}")
        for row in res:
            st.text(row)
