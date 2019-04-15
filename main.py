from microWebSrv import MicroWebSrv
import network
from machine import Pin, ADC


adc = ADC(Pin(33))  # fotoresist pin on board - 32

ssid = ''
password = ''
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
        if data < 700 or data == 4095:
            print(data)
            STATUS = "WC is invaded!"
        else:
            print(data)
            STATUS = "WC is vacant"
    except:
        STATUS = 'Attempting to read sensor...'
    httpResponse.WriteResponseOk(
        headers=({'Cache-Control': 'no-cache'}),
        contentType='text/event-stream',
        contentCharset='UTF-8',
        content='data: {0}\n\n'.format(STATUS))


def _acceptWebSocketCallback(webSocket, httpClient) :
    print("WS ACCEPT")
    webSocket.RecvTextCallback = _recvTextCallback
    webSocket.RecvBinaryCallback = _recvBinaryCallback
    webSocket.ClosedCallback = _closedCallback


def _recvTextCallback(webSocket, msg) :
    print("WS RECV TEXT : %s" % msg)
    webSocket.SendText("Reply for %s" % msg)


def _recvBinaryCallback(webSocket, data) :
    print("WS RECV DATA : %s" % data)


def _closedCallback(webSocket) :
    print("WS CLOSED")


#routeHandlers = [
#	( "/test",	"GET",	_httpHandlerTestGet ),
#	( "/test",	"POST",	_httpHandlerTestPost )
#]
# routeHandlers = [ ( "/dht", "GET",  _httpHandlerDHTGet ) ]


srv = MicroWebSrv(webPath='/www/')
srv.MaxWebSocketRecvLen = 256
srv.WebSocketThreaded = False
srv.AcceptWebSocketCallback = _acceptWebSocketCallback
srv.Start()
