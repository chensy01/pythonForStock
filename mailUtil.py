#!/usr/bin/python2.7
# -*- coding: utf-8 -*-  

from  email.mime.text import MIMEText
from  email.mime.image import MIMEImage
from  email.mime.multipart import MIMEMultipart
import smtplib

#发件人列表
to_list=["csy.mailbox@qq.com"]
#对于大型的邮件服务器，有反垃圾邮件的功能，必须登录后才能发邮件，如126,163
mail_server="smtp.126.com"         # 126的邮件服务器
mail_login_user="c520sy@126.com"   #必须是真实存在的用户
mail_passwd="csy.passto126"               #必须是对应上面用户的正确密码，我126邮箱对应的密码

def send_mail_with_attach(sub,content,file,attachName):
    '''
    to_list:发给谁
    sub:主题
    content:内容
    send_mail("aaa@126.com","sub","content")
    '''
    me=mail_login_user+"<"+mail_login_user+">"
    #msg = MIMEText(content)
    msg=MIMEMultipart()
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)


    image = MIMEImage(open(file,'rb').read())
    #image.add_header('Content-ID','<image>')
    image["Content-Type"] = 'application/octet-stream'  
    image["Content-Disposition"] = 'attachment; filename=' + attachName
    msg.attach(image)
    try:
        s = smtplib.SMTP()
        s.connect(mail_server)
        s.login(mail_login_user,mail_passwd)
        s.sendmail(me, to_list, msg.as_string())
        s.close()
        return True
    except Exception, e:
        print str(e)
        return False


def send_mail_without_attach(sub,content):
    '''
    to_list:发给谁
    sub:主题
    content:内容
    send_mail("aaa@126.com","sub","content")
    '''
    me=mail_login_user+"<"+mail_login_user+">"
    msg = MIMEText(content)
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)

    try:
        s = smtplib.SMTP()
        s.connect(mail_server)
        s.login(mail_login_user,mail_passwd)
        s.sendmail(me, to_list, msg.as_string())
        s.close()
        return True
    except Exception, e:
        print str(e)
        return False

if __name__ == '__main__':
    if send_mail("subject","content","/Users/momo/Programs/python/result/600573.png",'wanxiu.png'):
        print "发送成功"
    else:
        print "发送失败"