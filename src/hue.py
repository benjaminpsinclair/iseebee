def getCommand(decrypted):
    match decrypted[0:1].hex():
        case "01":
            return "\nCommand - Route Request"
        case "08":
            return "\nCommand - Link Status"
        case _:
            return "\nUnknown Command"
