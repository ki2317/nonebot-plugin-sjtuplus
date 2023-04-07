from nonebot import on_request, on_notice
from nonebot.adapters.onebot.v11 import MessageSegment, Event, Bot, GroupRequestEvent, GroupIncreaseNoticeEvent
import requests, re, httpx

dict1 = {}


def _check0(event: Event):
    return isinstance(event, GroupRequestEvent)


requ = on_request(rule=_check0)
# client = httpx.AsyncClient()


@requ.handle()
async def _(event: GroupRequestEvent, bot: Bot):
    code = event.comment
    code = re.findall(re.compile('答案：(.*)'), code)[0]
    headers = {'Api-Key': Api-Key}
    data = {"qq_number": str(event.user_id), "token": code}
    print(code)
    print(data)
    resp = requests.post("https://plus.sjtu.edu.cn/attest/verify", headers=headers, json=data)
    print(resp.content)
    if not str(resp.content).split(":")[1].split(",")[0].strip() == 'false':
        global dict1
        dict1['qid'] = event.user_id
        await bot.call_api("set_group_add_request", flag=event.flag, sub_type=event.sub_type, approve=True)
        await requ.finish()
    else:
        await bot.call_api("set_group_add_request", flag=event.flag, sub_type=event.sub_type,
                           approve=False, reason='认证错误，请确认您输入的SJTU+验证是否正确')
        await requ.finish()
