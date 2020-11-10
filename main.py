from fastapi import FastAPI

from config.locale import _

app = FastAPI()

@app.get('/')
async def root():
    return {'message': _('Hello!'), 'add': _('Add')}

@app.get('/en')
async def en():
    return {'message': _('Hello!')}

