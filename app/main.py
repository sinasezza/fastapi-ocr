from fastapi import FastAPI


app = FastAPI()


@app.get("/")
def home_view():
    return {"message": "Welcome to the FastAPI application!"}


@app.post("/")
def home_detail_view():
    return {"message": "Welcome to the FastAPI application! POST"}