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
        // we need to have a default constructor unparameterized.
    }
    Person(string name, int age) :
        name(name), age(age)
    {
    }

    void print() const
    {
        cout << name << ", " << age << endl;
    }

    bool operator<(const Person &other) const
    {
        // to make the iterator it work we need to overload the less than operator
        return name < other.name;
    }
};


int main(int argc, char* argv[])
{
    // custom maps as value
    map<int, Person> people;
    people[0] = Person("Emre", 30);
    people[1] = Person("Goku", 12);
    people[2] = Person("Vegeta", 42);

    for (map<int, Person>::iterator it = people.begin(); it != people.end(); it++)
    {
        it->second.print();
    }
    cout << endl;

    // custom maps as keys
    map<Person, int> engineers;
    engineers[Person("Emre", 30)] = 1;
    engineers[Person("Goku", 12)] = 2;
    engineers[Person("Vegeta", 42)] = 3;

    for (map<Person, int>::iterator it = engineers.begin(); it != engineers.end(); it++)
    {
        cout << it->second << ": " << std::flush;
        it->first.print();
        cout << endl;
    }

    return 0;
}
