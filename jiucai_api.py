# -*- coding: utf-8 -*-
from typing import List

import numpy as np
import requests
import uvicorn
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from jiucai import JiuCaiSpider
from pydantic import BaseModel, Field

news_agent_app = FastAPI()

jiucai_spider = JiuCaiSpider()
class JiucaiRequest(BaseModel):
    query: str
    items_num: int

@news_agent_app.post("/news_agent_app/get_jiucai_data")
def get_jiucai_data(ask: JiucaiRequest):
    jiucai_data = jiucai_spider.get_jiucai_data(query=ask.query, items_num=ask.items_num)
    return {
        "jiucai_data": jiucai_data
    }