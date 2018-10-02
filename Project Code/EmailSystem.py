import smtplib 
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import os

class Email:
	persona_email_id = 'mandloiankit377@gmail.com'
	persona_password = 'mummygoluki2'  
	receiver = ''
	msg = MIMEMultipart()
	s =None
	
	def __init__(self,str):
		self.msg = MIMEMultipart()
		self.receiver = str
		self.s = smtplib.SMTP('smtp.gmail.com', 587)
		self.s.starttls()  
		self.s.login(self.persona_email_id, self.persona_password) 
		self.msg['Subject'] = 'Recommendations from persona'
		self.msg['From'] = self.persona_email_id
		self.msg['To'] = self.receiver +'.cc'

	def send_mssg(self,data,img_paths=None): 
		text = MIMEText(data)
		self.msg.attach(text)
		if img_paths != None:
			for img in img_paths:
				file = open(img, 'rb')
				image = MIMEImage(file.read())
				file.close()
				self.msg.attach(image)
		self.s.sendmail(self.persona_email_id, self.receiver, self.msg.as_string()) 
		self.s.quit() 

