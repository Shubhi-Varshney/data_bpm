from fastapi import FastAPI

app = FastAPI()

'''
@app.get('/predict')
def suggestion(features):
    # Compute attendee course suggestion `
    course = 1 # compute course selection -> to be done

    return {'course': course}
'''



@app.get("/")
def root():
    return {
        "greeting": "works!"
    }
