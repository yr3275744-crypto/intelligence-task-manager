import uvicorn
from fastapi import FastAPI
from routes.agent_routes import router as agent_router
from routes.mission_routes import router as mission_router
from database.db_connection import DBConnection

DBConnection().create_database()
DBConnection(database="Intelligence_db").create_tables()

app = FastAPI()

app.include_router(agent_router)
app.include_router(mission_router)

if __name__ == "__main__":
    uvicorn.run(app)