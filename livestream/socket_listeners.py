socket_listeners = []


def addListener(connect_id):
    socket_listeners.append(connect_id)


def removeListener(connect_id):
    socket_listeners.remove(connect_id)


def getListenersAmount():
    return len(socket_listeners)
