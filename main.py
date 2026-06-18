import uvicorn
from fastapi import FastAPI
from routes.agent_routes import router as agent_router


app = FastAPI()

app.include_router(agent_router)

if __name__ == "__main__":
    uvicorn.run(app)