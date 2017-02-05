#pragma once

#include <iostream>
#include <string>
#include <vector>
using std::cin;
using std::cout;
using std::endl;
using std::flush;
using std::vector;
using std::string;


void stringVector(string message)
{
    // Setup single string
    vector<string> strings(20, message);
    for (unsigned int i = 0; i < strings.size(); i++)
    {
        // add number to the end
        strings[i] += std::to_string(i);
        cout << strings[i] << endl;
    }
}


void stringIterator()
{
    // using iterator object to traverse the vector
    vector<string> strings;
    strings.push_back("one");
    strings.push_back("two");
    strings.push_back("three");

    // using string iterator object which is a pointer to check for conditions from begin to end
    for (vector<string>::iterator it = strings.begin(); it != strings.end(); it++)
    {
        // dereference iterator pointer
        cout << *it << endl;
    }
    vector<string>::iterator it = strings.begin();
    // Should print out one
    cout << *it << endl;
    // Should print out two
    it++;
    cout << *it << endl;
    // Should print out three
    it++;
    cout << *it << endl;
}


void gridVector()
{
    // Create a vector in a vector array using a row and column example
    vector< vector<int> > grid(3, vector<int>(3, 0));
    for (unsigned int row = 0; row < grid.size(); row++)
    {
        for (unsigned int col = 0; col < grid[row].size(); col++)
        {
            cout << grid[row][col] << flush;
        }
        cout << endl;
    }
}


int main(int argc, char* argv[])
{
    stringVector("This is line number ");
    stringIterator();
    gridVector();
    return 0;
}
