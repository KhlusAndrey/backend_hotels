from fastapi import FastAPI


app = FastAPI()


@app.get('/')
def get_hotels():
    return 'hotels'
