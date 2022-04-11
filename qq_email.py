#! /usr/local/bin/python3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import httpx
from fake_headers import Headers
import json
import asyncio
from email.utils import parseaddr,formataddr
from email.header import Header



client = httpx.AsyncClient()
SEND_FROM = '649307714@qq.com'
TOKEN = 'whtsnnvdazthbfag'
SEND_TO = '649239257@qq.com'


def plain_mail():
    content = '用python发送的正文内容'
    email_content  = MIMEText(content, 'plain', 'utf-8')
    return email_content

def file_mail():
    with open(r'/Users/wangtao/pyseo/email/seo快排监控-2022.xlsx','rb') as f:
        file_data = f.read()
    file_content = MIMEText(file_data,'base64','utf-8')
    file_content.add_header('Content-Disposition', 'attachment', filename='seo快排监控-2022.xlsx')
    return file_content

def send_mail(email):
    smtp = smtplib.SMTP_SSL('smtp.qq.com', 465)
    smtp.login(SEND_FROM, TOKEN)
    email['From'] = formataddr((Header('a', 'utf-8').encode(3), '<wangtao@163.com>'))
    email['To'] = SEND_TO
    email['Subject'] = '淡墨流年发送的邮件内容'
    smtp.sendmail(SEND_FROM, SEND_TO, email.as_string())
    print('发送成功')
    smtp.quit()

def complex_mail(content,file_data):
    message = MIMEMultipart()
    message.attach(content)
    message.attach(file_data)
    return message

async def spider_qq():
    url = 'https://qun.qq.com/cgi-bin/qun_mgr/search_group_members'
    all_qq = []
    st = 0
    end = 20
    while True:
        from_data = {
            'gc': '47055885',
            'st': str(st),
            'end': str(end),
            'sort': '0',
            'bkn': '2003443861',
        }
        headers = Headers(headers=True).generate()
        headers['Cookie'] = 'pgv_pvid=5400314765; RK=L25EEkfa0p; ptcz=f5073fd96125928efb5ee960688f9ac1207510277dcff519a36c74cfc28e6b7a; iip=0; fqm_pvqid=bdaecdf1-1f6b-4b8e-8b39-328c2cca863e; _ga=GA1.2.608400023.1627873924; tvfe_boss_uuid=9f451a47f8348a21; o_cookie=649307714; gid=e88e04e6-a8cf-4865-9895-9b261e42f41a; pac_uid=1_649307714; ptui_loginuin=649307714; uin=o0649307714; skey=@0rzmBzXlg; _qpsvr_localtk=0.19626989067183165; p_uin=o0649307714; pt4_token=nvILNNRsGC7p8m9hUS7KpXM8ibFA4IHQkka57ypqYnY_; p_skey=hBV44XmG7AVvoGS40jCzF*QMQI7hgvob2WolDkM4JpU_; traceid=f7fc0812b4'
        res = await client.post(url=url,data=from_data,headers=headers)
        # print(json.dumps(res.json(),indent=2,ensure_ascii=False))
        try:
            info_qq = res.json()['mems']
            qq_list = [qq['uin']  for qq in info_qq]
            print(qq_list)
            all_qq.extend(qq_list)
        except:
            await client.aclose()
            break
        else:
            st += 21
            end = st + 20
            print(st,end)

    return all_qq

async def main():
    content = plain_mail()
    file_data = file_mail()
    complex_data = complex_mail(content,file_data)
    send_mail(complex_data)
    # qq_list = await spider_qq()
    file_mail()
if __name__ == '__main__':
    # send_mail()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())