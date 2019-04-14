from microWebSrv import MicroWebSrv
import time
import network
from machine import Pin, ADC



adc = ADC(Pin(33))  # fotoresist pin on board - 32


ssid = 'Addams_family'
password = '2gvI6hV%~$vea'
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())


STATUS = 'Loading'

@MicroWebSrv.route('/status')
def _httpHandlerDHTGet(httpClient, httpResponse):
    global STATUS
    try:
        data = adc.read()  # Poll sensor
        if data > 20:
            print(data)
            STATUS = "WC is invaded!"
        else:
            STATUS = "WC is vacant"
    except:
        STATUS = 'Attempting to read sensor...'
    httpResponse.WriteResponseOk(
        headers=({'Cache-Control': 'no-cache'}),
        contentType='text/event-stream',
        contentCharset='UTF-8',
        content='data: {0}\n\n'.format(STATUS))



# @MicroWebSrv.route('/dht')
# def _httpHandlerDHTGet(httpClient, httpResponse):
#     try:
#         sensor.measure()  # Poll sensor
#         t, h = sensor.temperature(), sensor.humidity()
#         print(t, h)
#         if all(isinstance(i, int) for i in [t, h]):  # Confirm values
#             data = '{0:.1f}&deg;C {1:.1f}%'.format(t, h)
#         else:
#             data = 'Invalid reading.'
#     except:
#         data = 'Attempting to read sensor...'
#     httpResponse.WriteResponseOk(
#         headers=({'Cache-Control': 'no-cache'}),
#         contentType='text/event-stream',
#         contentCharset='UTF-8',
#         content='data: {0}\n\n'.format(data))


# def _httpHandlerTestGet(httpClient, httpResponse) :
#     content = """\
#     <!DOCTYPE html>
#     <html lang=en>
#         <head>
#             <meta charset="UTF-8" />
#             <title>TEST GET</title>
#         </head>
#         <body>
#             <h1>TEST GET</h1>
#             Client IP address = %s
#             <br />
#             <form action="/test" method="post" accept-charset="ISO-8859-1">
#                 First name: <input type="text" name="firstname"><br />
#                 Last name: <input type="text" name="lastname"><br />
#                 <input type="submit" value="Submit">
#             </form>
#         </body>
#     </html>
#     """ % httpClient.GetIPAddr()
#     httpResponse.WriteResponseOk( headers		 = None,
#                                   contentType	 = "text/html",
#                                   contentCharset = "UTF-8",
#                                   content 		 = content )


# @MicroWebSrv.route('/test', 'POST')
# def _httpHandlerTestPost(httpClient, httpResponse) :
#     formData  = httpClient.ReadRequestPostedFormData()
#     firstname = formData["firstname"]
#     lastname  = formData["lastname"]
#     content   = """\
#     <!DOCTYPE html>
#     <html lang=en>
#         <head>
#             <meta charset="UTF-8" />
#             <title>TEST POST</title>
#         </head>
#         <body>
#             <h1>TEST POST</h1>
#             Firstname = %s<br />
#             Lastname = %s<br />
#         </body>
#     </html>
#     """ % ( MicroWebSrv.HTMLEscape(firstname),
#             MicroWebSrv.HTMLEscape(lastname) )
#     httpResponse.WriteResponseOk( headers		 = None,
#                                   contentType	 = "text/html",
#                                   contentCharset = "UTF-8",
#                                   content 		 = content )
#
#
# @MicroWebSrv.route('/edit/<index>')             # <IP>/edit/123           ->   args['index']=123
# @MicroWebSrv.route('/edit/<index>/abc/<foo>')   # <IP>/edit/123/abc/bar   ->   args['index']=123  args['foo']='bar'
# @MicroWebSrv.route('/edit')                     # <IP>/edit               ->   args={}
# def _httpHandlerEditWithArgs(httpClient, httpResponse, args={}) :
#     content = """\
#     <!DOCTYPE html>
#     <html lang=en>
#         <head>
#             <meta charset="UTF-8" />
#             <title>TEST EDIT</title>
#         </head>
#         <body>
#     """
#     content += "<h1>EDIT item with {} variable arguments</h1>"\
#         .format(len(args))
#
#     if 'index' in args :
#         content += "<p>index = {}</p>".format(args['index'])
#
#     if 'foo' in args :
#         content += "<p>foo = {}</p>".format(args['foo'])
#
#     content += """
#         </body>
#     </html>
#     """
#     httpResponse.WriteResponseOk( headers		 = None,
#                                   contentType	 = "text/html",
#                                   contentCharset = "UTF-8",
#                                   content 		 = content )

# ----------------------------------------------------------------------------

def _acceptWebSocketCallback(webSocket, httpClient) :
    print("WS ACCEPT")
    webSocket.RecvTextCallback   = _recvTextCallback
    webSocket.RecvBinaryCallback = _recvBinaryCallback
    webSocket.ClosedCallback 	 = _closedCallback

def _recvTextCallback(webSocket, msg) :
    print("WS RECV TEXT : %s" % msg)
    webSocket.SendText("Reply for %s" % msg)

def _recvBinaryCallback(webSocket, data) :
    print("WS RECV DATA : %s" % data)

def _closedCallback(webSocket) :
    print("WS CLOSED")

# ----------------------------------------------------------------------------

#routeHandlers = [
#	( "/test",	"GET",	_httpHandlerTestGet ),
#	( "/test",	"POST",	_httpHandlerTestPost )
#]
# routeHandlers = [ ( "/dht", "GET",  _httpHandlerDHTGet ) ]


srv = MicroWebSrv(webPath='/www/')
srv.MaxWebSocketRecvLen     = 256
srv.WebSocketThreaded		= False
srv.AcceptWebSocketCallback = _acceptWebSocketCallback
srv.Start()

# ----------------------------------------------------------------------------
