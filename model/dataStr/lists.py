import utils

class queue:

    __qList: list


    def __init__(self, queue: list = []):
        self.__qList = list

    def enqueue(self, element):
        self.__qList.append(element)
    

    def dequeue(self):
        if len(self.__qList) == 0:
            return None
        element = self.__qList[0]
        self.__qList.pop(0)

        return element


    def size(self):
        return len(self.__qList)

    
    def peek(self):
        if self.size == 0:
            return None
        return self.__qList[0]
    

class stack:
    __sList : list


    def __init__(self, stack: list = []):
        self.__sList = list
    

    def push(self, element):
        self.__sList.append(element)

    
    def pop(self):
        if len(self.__sList) == 0:
            return None
        element = self.__sList[-1]
        self.__sList.pop()

        return element

    
    def size(self):
        return len(self.__sList)

    
    def top(self):
        if self.size == 0:
            return None
        return self.__sList[-1]
    

class tokens(queue):
    def dequeue(self):
        element = super().dequeue()
        if element is None:
            utils.SyntaxError("Fin del archivo inesperado.")
        return element
    

class scope(stack):
    def pop(self):
        element = super().pop()
        if element is None:
            utils.SyntaxError("Fin del archivo inesperado.")
        return element