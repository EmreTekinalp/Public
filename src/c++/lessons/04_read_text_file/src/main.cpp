#pragma once

#include <iostream>
#include <fstream>
#include <string>

using std::cin;
using std::cout;
using std::endl;
using std::string;
using std::ifstream;


string getFile(string fileName)
{
    // Get the file name by grabbing the README.txt inside the src dir
    char path[] = __FILE__;
    *(strrchr(path, '\\') + 1) = 0;
    string filePath;
    filePath += path;
    filePath += fileName;
    return filePath;
}


int main(int argc, char* argv[])
{
    string inFileName = getFile("README.txt");
    ifstream inFile;

    inFile.open(inFileName);

    if (inFile.is_open())
    {
        string line;
        while (inFile)
        {
            getline(inFile, line);
            cout << line << endl;
        }
        inFile.close();
    }
    else
    {
        cout << "Cannot open file: " << inFileName << endl;
    }

    return 0;
}
