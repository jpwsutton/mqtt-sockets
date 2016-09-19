import paho.mqtt.client as mqtt
import json
from pprint import pprint
import pi_switch

# Get configuration data
with open('config.json') as data_file:
    config = json.load(data_file)

def on_connect(mqttc, obj, flags, rc):
    print("Connected, rc: "+str(rc))

def on_message(mqttc, obj, msg):
    socket = config['sockets'][msg.topic]
    payload = json.loads(msg.payload.decode("utf-8"))
    pprint(socket)
    print("Message arrived for socket: " + socket['name'] + " : " + str(payload))
    if socket['type'] is 'RAW':
        sender = pi_switch.RCSwitchSender()
        sender.enableTransmit(config['transmitterPin'])
        if(payload['state'] is 1):
            print("Turned On using RAW command.")
            sender.send(socket['onCommand'])
        else:
            print("Turned off using RAW command.")
            sender.send(socket['offCommand'])
    elif socket['type'] is 'B':
        if(payload['state'] is 1):
            print("Turned on using Type B command.")
            switch = pi_switch.RCSwitchB(socket['group'], socket['switch'])
            switch.enableTransmit(config['transmitterPin'])
            switch.switchOn()
        else:
            print("Turned off using Type B command.")
            switch = pi_switch.RCSwitchB(socket['group'], socket['switch'])
            switch.enableTransmit(config['transmitterPin'])
            switch.switchOff()


def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

def on_log(mqttc, obj, level, string):
    print(string)


print("Connecting to Host %s" % config['mqttConfig']['server'])

# If you want to use a specific client id, use
# mqttc = mqtt.Client("client-id")
# but note that the client id must be unique on the broker. Leaving the client
# id parameter empty will generate a random id for you.
mqttc = mqtt.Client(client_id=config['mqttConfig']['clientId'], protocol="MQTTv311", clean_session=True)
mqttc.username_pw_set(config['mqttConfig']['username'], password=config['mqttConfig']['password'])
if "cafile" in config['mqttConfig']:
    mqttc.tls_set('./' + config['mqttConfig']['cafile'])
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
# Uncomment to enable debug messages
#mqttc.on_log = on_log
mqttc.connect(config['mqttConfig']['server'], config['mqttConfig']['port'], 60)

for key in config['sockets']:
    print('Subscribing to %s' % key)
    mqttc.subscribe(key, 0)


mqttc.loop_forever()
