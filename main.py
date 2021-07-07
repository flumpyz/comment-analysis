# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from sentiment_determinant import SentimentDeterminant
from visualizer import Visualizer
import commentParser as cp
import check_date as cd


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    comments = SentimentDeterminant.get_sentiment_array_from_file()
    Visualizer.build_a_schedule(comments)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
