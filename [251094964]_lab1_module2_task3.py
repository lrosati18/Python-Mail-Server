from socket import *
import base64
import ssl

# Message to be sent in the body of the email
msg = "\r\n I love computer networks!" 
endmsg = "\r\n.\r\n"


# Choose a mail server (e.g. Google mail server) and call it mailserver 
mailserver = "smtp.gmail.com"
port = 587 #Using TLS 


# Create socket called clientSocket and establish a TCP connection with mailserver
clientSocket = socket(AF_INET, SOCK_STREAM) 
clientSocket.connect((mailserver,port))

recv = clientSocket.recv(1024).decode() 
print(recv)
if recv[:3] != '220':
    print('220 reply not received from server.')


# Send HELO command and print server response. 
heloCommand = 'HELO Alice\r\n' 
clientSocket.send(heloCommand.encode())

recv1 = clientSocket.recv(1024).decode() 
print(recv1)
if recv1[:3] != '250':
    print('250 reply not received from server.')

#Start TLS
command = "STARTTLS\r\n"
clientSocket.send(command.encode())

recv2 = clientSocket.recv(1024).decode()
print(recv2)
if recv2[:3] != '220':
    print('220 reply not received from server.')

# Wrap clientSocket in SSL for security purposes, it is now renamed sslSocket    
sslSocket = ssl.wrap_socket(clientSocket, ssl_version = ssl.PROTOCOL_SSLv23)

#Authentication login command (username and password)
username = "lilianatest52@gmail.com"
password = "Ece4436!"
base64_str = ("\x00"+username+"\x00"+password).encode()
base64_str = base64.b64encode(base64_str)
authMsg = "AUTH PLAIN ".encode()+base64_str+"\r\n".encode()
sslSocket.send(authMsg)
recv3 = sslSocket.recv(1024)
print('Auth Response: ' + recv3.decode())


# Send MAIL FROM command and print server response.
mailFrom = 'MAIL FROM:<lilianatest52@gmail.com>\r\n'
sslSocket.send(mailFrom.encode())
recv4 = sslSocket.recv(1024).decode()
print(recv4)

if recv4[:3] != '250': 
    print('250 reply not received from server.')


# Send RCPT TO command and print server response.
rcptTo = 'RCPT TO:<lilianatest52@gmail.com>\r\n'
sslSocket.send(rcptTo.encode()) 
recv5= sslSocket.recv(1024).decode()
print(recv5)

if recv5[:3] != '250': 
    print('250 reply not recieved from server.')


# Send DATA command and print server response.
data = 'DATA \r\n'
sslSocket.send(data.encode())
recv6 = sslSocket.recv(1024).decode()
print(recv6)

if recv6[:3] != '250': 
    print('250 reply not received from server.')


# Send message data.
sslSocket.send(msg.encode())
sslSocket.send(endmsg.encode())
recv7 = sslSocket.recv(1024).decode()
print(recv7)

if recv7[:3] != '250': 
    print('250 reply not received from server.') 


# Message ends with a single period.
endmsg = '\r\n.\r\n'
sslSocket.send(msg.encode())
sslSocket.send(endmsg.encode())
recv8 = sslSocket.recv(1024).deocde()
print(recv8)

if recv8[:3] != '354': 
    print('354 reply not received from server.') 


# Send QUIT command and get server response.
sslSocket.send("QUIT\r\n".encode())
recv9 = sslSocket.recv(1024).decode()
print(recv9)
sslSocket.close() 

if recv9[:3] != '221':
    print('221 reply not received from server.')
