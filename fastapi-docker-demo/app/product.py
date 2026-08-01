from fastapi import FastAPI

data =FastAPI(title="employe details")

# result=[]

@data.get("/getEmployees")
def getemployees():
    return "all employees are good"