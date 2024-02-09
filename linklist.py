class MyLinkedList:

    def __init__(self):

        self.head = None 

    def get(self, index: int) -> int:

        current = self.head
        for i in range (index):
            if current:
                current = current.next
            else:
                return -1
        return current.val
        
    def addAtHead(self, val: int) -> None:

        new_node = Node(val, self.head)
        self.head = new_node
        
    def addAtTail(self, val: int) -> None:

        new_node = Node(val, None)

        if self.head == None:
            self.head = new_node
        
        current = self.head 
        while current.next:
            current = current.next
        current.next = new_node

    def addAtIndex(self, index: int, val: int) -> None:
        
        current = self.head
        new_node = Node(val, None)
        for i in range (index):
            if current:
                current = current.next
            else:
                return -1
        next_node = current.next
        current.next = new_node
        new_node.next = next_node

    def deleteAtIndex(self, index: int) -> None:

        current = self.head 
        
        for i in range (index - 1):
            if current:
                current = current.next
            else:
                return -1

        next_node = current.next
        next_next_node = next_node.next
        current.next = next_next_node
        
    def view(self):
        
        current = self.head
        
        while current:
            print(current.val)
            current = current.next
        

class Node:
    
    def __init__(self, val, next):

        self.val = val
        self.next = next
        
myLinkedList = MyLinkedList()
myLinkedList.addAtHead(1)
myLinkedList.addAtTail(3)
myLinkedList.addAtIndex(1, 2)  # linked list becomes 1->2->3
myLinkedList.get(1)           # return 2
myLinkedList.deleteAtIndex(1)  # now the linked list is 1->3
myLinkedList.get(1)   