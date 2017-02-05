#pragma once

#include <iostream>
#include <list>
using std::cin;
using std::cout;
using std::endl;
using std::list;

int main(int argc, char* argv[])
{
    // declare and initialize int list
    list<int> numbers;
    numbers.push_back(1);
    numbers.push_back(2);
    numbers.push_back(3);
    numbers.push_front(0);

    // access values via iterator and insert value 100
    list<int>::iterator it = numbers.begin();
    it++;
    numbers.insert(it, 100);
    cout << *it << endl;

    // Iterate list via iterator
    cout << "Iterate list:" << endl;
    for (list<int>::iterator it = numbers.begin(); it != numbers.end(); it++)
    {
        cout << *it << endl;
    }

    // erase value 100 from int list via iterator
    list<int>::iterator eraseIt = numbers.begin();
    eraseIt++;
    eraseIt = numbers.erase(eraseIt);

    // erase value from int list via iterator in a for loop when value is 2
    cout << "Iterate list via eraseIt:" << endl;
    for (list<int>::iterator eraseIt = numbers.begin(); eraseIt != numbers.end();)
    {
        if (*eraseIt == 2)
        {
            eraseIt = numbers.erase(eraseIt);
        }
        else
        {
            eraseIt++;
        }
    }

    // print out modified list
    for (list<int>::iterator it = numbers.begin(); it != numbers.end(); it++)
    {
        cout << *it << endl;
    }
    return 0;
}
