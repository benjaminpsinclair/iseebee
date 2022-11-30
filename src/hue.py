def getCommand(decrypted):
    match decrypted[0:1]:
        case b'\x01':
            return "Route Request"
        case b'\x08':
            return "Link Status"
        case _:
            return "Unknown Command"
