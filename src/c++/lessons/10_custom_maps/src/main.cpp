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


class Person
{
private:
    string name;
    int age;
public:
    Person()
    {
    }
    Person(string name, int age) :
        name(name), age(age)
    {
    }

    void print()
    {
        cout << name << ", " << age << endl;
    }
};


int main(int argc, char* argv[])
{
    map<int, Person> people;
    people[0] = Person("Emre", 30);
    people[1] = Person("Goku", 12);
    people[2] = Person("Vegeta", 42);

    for (map<int, Person>::iterator it = people.begin(); it != people.end(); it++)
    {
        it->second.print();
    }

    return 0;
}
