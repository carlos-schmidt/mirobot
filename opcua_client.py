import opcua

url = 'opc.tcp://192.168.1.1:4840'

client = opcua.Client(url=url)

servers = client.connect_and_find_servers()

print(servers)