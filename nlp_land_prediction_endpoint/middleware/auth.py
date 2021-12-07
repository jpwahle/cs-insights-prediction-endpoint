from fastapi import FastAPI, Request, HTTPException

def get_user(token: str) -> dict: ## TODO change return value from dict to User model
    ## TODO implement concrete functionality, to get the user from the NLP-backend
    return token

async def check_auth(request: Request, call_next):
    request.state.user = None
    if 'authorization' in request.headers:
        request.state.user = get_user(request.headers['authorization'])
    response = await call_next(request)
    return response
