from publisher import Publisher
from subscriber import Subscriber
import uuid

class ServidorCentral(Subscriber, Publisher):

    def __init__(self):
        self.server_id       = uuid.uuid1()
        self.stations_ids    = []
        self.stations_queues = []

    # It returns location of x in given array arr
    # if present, else returns -1
    def binarySearch(arr, left, right, value_to_be_searched):
        while left <= right:
            mid = left + (right - left) // 2
            # Check if value to be searched is present at mid
            if arr[mid] == value_to_be_searched:
                return mid
            # If value to be searched is greater, ignore left half
            elif arr[mid] < value_to_be_searched:
                left = mid + 1
            # If value to be searched is smaller, ignore right half
            else:
                right = mid - 1
        # If we reach here, then the element
        # was not present
        return -1


    def receive_message_from_station(self):
        ...

    def publish_message_to_cars(self):
        ...

    def process_better_station(self):
        # SEMPRE INSERE NA PRIMEIRA POSIÇÃO O POSTO COM A MENOR FILA
        self.stations_queues.insert(0, self.binarySearch(self.stations_queues))