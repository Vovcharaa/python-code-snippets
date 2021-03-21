from typing import Dict, Union
import pydantic
import aiohttp
import orjson
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

app = FastAPI(default_response_class=ORJSONResponse)   # set default response encoder


class TestBody(pydantic.BaseModel):
    length: int
    age: int
    name: str


def orjson_request(body: pydantic.BaseModel, headers: Union[Dict[str, str], None] = None):
    """
    orjson returns bytes instead of str which make it incompatable with aiohttp without .decode()
    To avoid dublicating of .encode() this function make valid body and header for json request
    """
    bytes_body = orjson.dumps(body.dict())
    content_type = {"content-type": "application/json"}
    if headers is not None:
        final_headers = {**content_type, **headers}    # final_headers = content_type | headers (for python 3.9+)
    else:
        final_headers = content_type
    return {"data": bytes_body, "headers": final_headers}


async def make_request():
    print(1)
    test_body = TestBody(length=2, age=5, name="pathetic")
    http = aiohttp.ClientSession()
    async with http.post(
        url="http://localhost/test",
        **orjson_request(test_body)
    ) as resp:
        body = await resp.json(loads=orjson.loads)    # load with orjson
    await http.close()
    return body


@app.post("/test")
async def test(body: TestBody):
    resp = await make_request()
    return resp
