class IterableStructure:
    """
    Class that implements an iterable structure
    """
    def __init__(self):
        self.__index = 0
        self.__list = []

    def __iter__(self):
        """
        Method that returns an iterator for the given object
        """
        return iter(self.__list)

    def __next__(self):
        """
        Method used to  iterate through all the items of an iterator. When we reach the end and there is no more data
        to be returned, it will raise the StopIteration Exception.
        """
        if self.__index + 1 >= self.__list.__len__():  # no more elements
            raise StopIteration
        self.__index += 1
        return self.__list[self.__index]

    def __len__(self):
        """
        Method that returns the length of the list
        """
        return len(self.__list)

    def __getitem__(self, index):
        """
        Method that gets the element from position <index>
        """
        return self.__list[index]

    def __setitem__(self, index, value):
        """
        Method that sets the value of the element on position <index>
        """
        self.__list[index] = value

    def __delitem__(self, index):
        """
        Method that deletes the element from position <index>
        """
        del self.__list[index]

    def append(self, element):
        """
        Method that appends an element to the list
        """
        self.__list.append(element)

    def get_list(self):
        """
        Method that returns the list
        """
        return self.__list[:]

    def clear(self):
        """
        Method that clears data
        """
        self.__list.clear()


"""
SORT
"""


def get_next_gap(gap):
    gap = (gap*10)//13
    if gap < 1:
        return 1
    return gap


def comb_sort(listt, function):
    """
    This function sorts elements of list by using a comparison function to determine order of elements.
    I used comb sort, which is an improvement of bubble sort. So, we start with the gap between 2 elements equal to
    length of list and then, at each iteration we decrease the gap by a "shrinking factor" of 1.3, which was found
    by testing the algorithm on a large number of lists.
    """
    length = len(listt)   # compute length of list
    gap = length          # initialize gap
    swap = True           # initialize swap to make sure loop runs at least once
    while gap != 1 or swap is True:  # run loop until gap gets 1 or there was no swap, meaning list is sorted
        gap = get_next_gap(gap)      # find next gap by decreasing last one by 1.3
        swap = False                 # set swap to false to check if any elements where swapped
        for i in range(0, length-gap):    # go through each section of list
            if function(listt[i], listt[i+gap]) is False:  # elements found at distance <gap> are not in order
                aux = listt[i]
                listt[i] = listt[i+gap]
                listt[i+gap] = aux
                swap = True          # swap elements and set swap to true to mark that there was a change, so elements
                                     # were not sorted yet


"""
FILTER
"""


def filter_list(listt, criteria):
    """
    This function filters elements of list by using a criteria to determine which elements are kept and stored in a new
    list and which ones are discarded.
    """
    new_list = []
    for i in range(len(listt)):
        if criteria(listt[i]) is True:
            new_list.append(listt[i])
    return new_list[:]
