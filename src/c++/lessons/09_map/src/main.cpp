#pragma once

#include <iostream>
#include <map>
#include <string>
#include <typeinfo>
#include <sstream>
using std::cin;
using std::cout;
using std::endl;
using std::map;
using std::string;
using std::make_pair;
using std::pair;
using std::stringstream;

int main(int argc, char* argv[])
{
    map<string, int> dict;
    string abc = "abcdefghijklmnopqrstuvwxyz";
    for (unsigned int i = 0; i < 10; i++)
    {
        /*
        string letter;
        letter += abc[i];
        pair<string, int> addToMap(std::to_string(abc[i]), i);
        stringstream ss;
        ss << abc[i];
        ss >> letter;
        cout << typeid(abc[i]).name() << ", " << typeid(ss).name() << endl;
        dict.insert(make_pair(letter, i));
        */
        // Crazy you need to store abc[i] first in a char type object
        // Then you create a string and do the conversion, then it is actual a string object!!! Crazy!!!
        char charLetter = abc[i];
        string letter;
        letter += charLetter;
        dict[letter] = i;
    }

    for (map<string, int>::iterator it = dict.begin(); it != dict.end(); it++)
    {
        cout << typeid(it->first).name() << ", " << it->first << ", " << it->second << endl;
    }

    for (map<string, int>::iterator it = dict.begin(); it != dict.end(); it++)
    {
        pair<string, int> element = *it;
        cout << element.first << ", " << element.second << endl;
    }

    return 0;
}
