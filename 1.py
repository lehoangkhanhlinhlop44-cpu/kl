import os
#Define the template
template = """
<html>
<head>
    <title>Hoàn trả đơn số {{ order_no }} của {{ name }}</title>
</head>
<body>
    <h2>Xin lỗi về {{ problem }}</h2>
    <p>
        Chúng tôi muốn xin lỗi vì {{ problem }} và chúng tôi muốn hoàn lại tiền<br>
        số tiền: {{ amount }} để mua {{ product }} mà bạn đã thực hiện thanh toán với chúng tôi.
    </p>
    <p>Phát hành bởi {{ name_of_company }} về mã order_no {{ order_no }}</p>
</body>
</html>
"""#creating the email_templates directory and html template
os.makedirs("SS5/emails_template/html_template")
with open("SS5/emails_template/html_template/apologize_email.html",'w',encoding='utf-8') as f:
    f.write(template)
    print('save as html file done')

os.makedirs("SS5/emails_template/plain_text")
with open("SS5/emails_template/plain_text/apologize_email.txt",'w',encoding='utf-8') as f:
    f.write(template)
    print('save as text file done')
