#pragma once

#include <iostream>
#include <fstream>
#include <string>
using std::cin;
using std::cout;
using std::endl;
using std::string;
using std::ofstream;
using std::ifstream;

// With pragma pack you are removing the padding
// which is a great optimization trick.
#pragma pack(push, 1)

struct Person
{
    char name[40];
    int age;
    double weight;
};

#pragma pack(pop)


int main(int argc, char* argv[])
{
    Person sensei = { "Johnny", 34, 89.5 };
    string fileName = "setup.bin";

    // Write binary file
    ofstream outFile;
    outFile.open(fileName, std::ios::binary);
    if (outFile.is_open())
    {
        outFile.write(reinterpret_cast<char*>(&sensei), sizeof(Person));
        outFile.close();
    }
    else
    {
        cout << "Could not create file: " << fileName << endl;
    }

    // Read binary file
    Person gakuse = {};
    ifstream inFile;
    inFile.open(fileName, std::ios::binary);
    if (inFile.is_open())
    {
        inFile.read(reinterpret_cast<char*>(&gakuse), sizeof(Person));
        inFile.close();
    }
    else
    {
        cout << "Could not read file: " << fileName << endl;
    }

    cout << gakuse.age << ", " << gakuse.name << ", " << gakuse.weight << endl;
    return 0;
}
