from twilio.rest import Client

# Twilio setup
accountSID = 'AC18538d56754b7aee7d26cf257cd79e39'
authToken = '4883475127d40d9b55e02dc989d4866e'
twilioCli = Client(accountSID, authToken)
myTwilioNumber = '+442030954125'
myCellPhone = '+447554662054'


reminder = 'Reminder!! Only 2 hours left to make picks! conorspicer.pythonanywhere.com'

numbers = ['+447917751419', '+447554662054']

for num in numbers:
    message = twilioCli.messages.create(body=saythis, from_=myTwilioNumber, to=num)
