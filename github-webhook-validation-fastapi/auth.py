import hmac
from fastapi import Header, HTTPException, Request, FastAPI, Depends

GITHUB_WEBHOOK_TOKEN = "some_super_secret_string"


# use as route dependency
async def validate_github(request: Request, x_hub_signature_256: str = Header(...)):
    signature = hmac.new(
        GITHUB_WEBHOOK_TOKEN.encode(), msg=await request.body(), digestmod="sha256"
    ).hexdigest()
    if not hmac.compare_digest(f"sha256={signature}", x_hub_signature_256):
        err = {"stack": "Validation failed"}
        raise HTTPException(403, err)


app = FastAPI(docs_url=None, redoc_url=None)

@app.post("/webhoook", dependencies=[Depends(validate_github)])
async def github_webhook(request: Request):
    body = await request.json()  # or form
    # do something
    print(body)

    return "ok"
