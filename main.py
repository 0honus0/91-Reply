import requests,re,os
from time import sleep
import logging
from random import randint
from multiprocessing import Pool
logging.basicConfig(format='%(asctime)s--%(levelname)s--%(message)s', level=logging.INFO)

#自行通过 https://f0416.wonderfulday30.live/my.php?item=posts 查看是否回复成功
#cookies只需要获取 CzG_auth 字段即可,如果不会获取自行百度 or 谷歌
#编辑 number 设置回复次数
#编辑 message 设置回复消息

number=10
message=['顶顶顶顶']
cookies=['CzG_auth=8c012t8QeOuKwdUn0CyTTbSJy7lGdR%2BNrhmxi2SVGySeeKrSlMgH8Ok%2B%2BzaFLjIuq7wnGXgKMLrECX3%2FTOjD7VbXH3kg','CzG_auth=253foW0whCGcqxtYdKfjE%2FpPuGgE2llaxMRKlVGzp5g8W8uNGqBCHi5zTo79CW5AOFVOgOjlyXiaqkVsAVG06vyDhEdn']

def reply(cookies,i):
    global number
    zipaidaren='https://f0416.wonderfulday30.live/forumdisplay.php?fid=19&page=1'
    yuanchuanzipai='https://f0416.wonderfulday30.live/forumdisplay.php?fid=4&page=1'
    woaiwoqi='https://f0416.wonderfulday30.live/forumdisplay.php?fid=21&page=1'

    bankuai=[zipaidaren,yuanchuanzipai,woaiwoqi]
    all_url=[]
    for key in bankuai:
        fid_pat='fid=(\d+)&'
        fid=re.search(fid_pat,key).group(1)
        headers={
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'en,zh-CN;q=0.9,zh;q=0.8,en-US;q=0.7',
            'cookie': cookies,
            'referer': key,
            'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
            'sec-ch-ua-mobile': '?0',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
            }
        res=requests.get(url=key,headers=headers)         
        res=res.content.decode("utf-8")
        if '登录' in res:
            logging.error('cookie无效，请更换cookie!!!')
            os._exit(0)
        pat='a href="(viewthread.php?[\s\S]*?)"'
        zhuti=res.find('版块主题')
        all_href=re.findall(pat,res[zhuti:])
        all_href=[href for href in all_href if 'page=' not in href]
        author_pat='<a href="space.php\?uid=\d+">([\s\S]*?)</a>'
        all_author=re.findall(author_pat,res[zhuti:])
        all_author=[all_author[i] for i in range(len(all_author)) if i%2==0]
        remove_list=[]
        for io in range(len(all_author)):
            if all_author[io]=='admin':
                remove_list.append(all_href[io])
        for remove in remove_list:
            all_href.remove(remove)
        all_ur=[href for href in all_href]
        for ur in all_ur:
            tid_pat='tid=(\d+)&'
            tid=re.search(tid_pat,ur).group(1)
            all_url.append([fid,tid])
    count=len(all_url)
    formhash_pat='name="formhash" value="(\w+)"'
    formhash=re.search(formhash_pat,res).group(1)
    logging.info('第'+str(i+1)+'个formhash值为:'+formhash)
    logging.info('第'+str(i+1)+'个获取帖子数量:'+str(count))
    logging.info('第'+str(i+1)+'个设置回帖数量为:'+str(number))
    logging.info('第'+str(i+1)+'个开始回复。。。')
    flag=1

    while number>0:
        ran=randint(0,count-1)
        url=all_url[ran]
        logging.info('第'+str(i+1)+'个开始回复第 '+str(flag)+' 条')
        logging.info('第'+str(i+1)+'个回复帖子fid,tid为: '+str(url[0])+' '+str(url[1]))
        url='https://f0416.wonderfulday30.live/post.php?action=reply&fid='+str(url[0])+'&tid='+str(url[1])+'&extra=page%3D1&replysubmit=yes&infloat=yes&handlekey=fastpost&inajax=1'
        reply_message=message[randint(0,len(message)-1)]
        logging.info('第'+str(i+1)+'个回复消息为:'+reply_message)
        headers={
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',        'accept-language': 'en,zh-CN;q=0.9,zh;q=0.8,en-US;q=0.7',
            'cache-control': 'max-age=0',
            'content-length': '190',
            'content-type': 'application/x-www-form-urlencoded',
            'cookie': cookies,
            'origin': 'https://f0416.wonderfulday30.live',
            'referer': url,
            'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
            'sec-ch-ua-mobile': '?0',
            'sec-fetch-dest': 'iframe',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
        }
        data={
            'formhash': str(formhash),
            'subject': '',
            'usesig': '0',
            'message': reply_message
        }
        res=requests.post(url=url,headers=headers,data=data)
        res=res.content.decode("utf-8")
        if '本站规定会员每小时最多只能发表 2 个帖子' in res:
            sleep_time=randint(600,1200)
            logging.warning('第'+str(i+1)+'个第 '+str(flag)+' 条回复失败,每小时只能回复2次,开始 sleep '+str(sleep_time)+' 秒')
            sleep(sleep_time)
            continue
        elif '您的回复已经发布' in res:
            number-=1
            flag+=1
            del all_url[ran]
            count-=1
            sleep_time=randint(1800,2000)
            logging.info('第'+str(i+1)+'个第 '+str(flag-1)+' 条回复成功,开始 sleep '+str(sleep_time)+' 秒')
            sleep(sleep_time)
        elif '两次发表间隔少于 60 秒' in res:
            logging.info('第'+str(i+1)+'个回复过快,程序出bug了,请勿在短时间内多次运行')
            os._exit(0)  
        else:
            logging.warning('第'+str(i+1)+'个未知返回,请通过日志判断')
            logging.info(res)
            os._exit(0)


p=Pool(len(cookies))
for i in range(len(cookies)):
    res=p.apply_async(reply,args=[cookies[i],i])
    print('第',str(i+1),'个进程启动.。。')
p.close()
p.join()
logging.warning(res.get())          #查看错误信息
logging.info('完成')