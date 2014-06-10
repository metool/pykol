import kol.Error as Error
from GenericRequest import GenericRequest
from kol.manager import PatternManager
from kol.database import ItemDatabase

class UseItemRequest(GenericRequest):
    def __init__(self, session, itemId):
        super(UseItemRequest, self).__init__(session)
        self.url = session.serverURL + "inv_use.php?pwd=" + session.pwd + "&whichitem=" + str(itemId)

    def parseResponse(self):
        # Check for items first
        items = []
        itemsAcquiredPattern = PatternManager.getOrCompilePattern("acquireItemFromItemUse")
        for match in itemsAcquiredPattern.finditer(self.responseText):
            itemID = int(match.group(1))
            item = ItemDatabase.getOrDiscoverItemFromId(itemID, self.session)
            items.append(item)
        if len(items):
            self.responseData["items"] = items
        
        # Check for meat gained
        gainMeatPattern = PatternManager.getOrCompilePattern("gainMeat")
        for match in gainMeatPattern.finditer(self.responseText):
            self.responseData["meat"] = match.group(1)
        
        # Check if we don't have the item
        notEnoughPattern = PatternManager.getOrCompilePattern("notEnoughItems")
        notEnoughMatch = notEnoughPattern.search(self.responseText)    
        if notEnoughMatch:
            raise Error.Error("You don't appear to have that item")
        
        if not len(self.responseData):
            print self.responseText
