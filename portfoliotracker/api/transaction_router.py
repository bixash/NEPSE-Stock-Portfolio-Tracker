"""
-- Created by: Ashok Kumar Pant
-- Created on: 7/18/23
"""

import logging

from fastapi import APIRouter

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("/transactions")
def predict(req: ConvAIRequest) -> BaseResponse:
    try:
        kwobjs = None
        if req.input_kwobjs is not None:
            kwobjs = map_to_input_kwobjs_pb(req.input_kwobjs)
        kwargs = None
        if req.input_kwargs is not None:
            kwargs = map_to_input_kwargs_pb(req.input_kwargs)
        r = ConvAIBaseRequest(inputText=req.input_text, taskType=req.task_type, inputKWObjs=kwobjs, inputKWArgs=kwargs,
                              prompt=req.prompt, temperature=req.temperature)
        res = CONV_AI_CLIENT.internal_getConvAIReply(r)
        return BaseResponse(error=res.error, msg=res.message, result=proto_to_json(res))
    except Exception as e:
        logger.error(f"Error in prediction: {str(e)}")
        return BaseResponse(error=True, msg=str(e), result=None)
