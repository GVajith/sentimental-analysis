
from fastapi import FastAPI
from router import router as social_router

app = FastAPI(title="Social Sentiment Pipeline")
app.include_router(social_router)

@app.get("/")
def root():
    return {"msg": "Use POST /social/pipeline to run the full pipeline and get a CSV back."}
