import uvicorn

if __name__ == "__main__":
    uvicorn.run("panchanga_app.api.main:app", host="0.0.0.0", port=8000, reload=True)
