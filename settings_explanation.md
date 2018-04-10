## memory/settings.py  

#### NEED_CERTIFICATE
if your hadoop cluster need certificate, set it to True

#### KEYTAB_PATH
if NEED_CERTIFICATE=True, set KEYTAB_PATH to where you have put your keytab file  
if NEED_CERTIFICATE=False, set to ''  

#### PRINCIPAL
if NEED_CERTIFICATE=True, set PRINCIPAL to your kerberos user name  
if NEED_CERTIFICATE=False, set to ''  

#### SERVER_PORT
IML-Predictor is a web application, which need a port number

#### ImpalaConstants
- Host: Impala instance address
- Port: Impala instance port
- User: Your Impala Username
- Version: Imapala version

