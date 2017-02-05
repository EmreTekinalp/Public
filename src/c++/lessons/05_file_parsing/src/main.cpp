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
    // We need the file path first to access the data
    char path[] = __FILE__;
    *(strrchr(path, '\\') + 1) = 0;
    string filePath;
    filePath += path + fileName;
    return filePath;
}


int main(int argc, char* argv[])
{
    string inFileName = getFile("abbreviations.config");
    ifstream inFile;

    cout << inFileName << endl;
    inFile.open(inFileName);

    if (inFile.is_open())
    {

        while (inFile)
        {
            string result, line;
            getline(inFile, line, ':');
            inFile >> result;
            cout << result << endl;
            if (!inFile)
            {
                break;
            }
        }
        inFile.close();


    }
    else
    {
        cout << "Could not open file: " << inFileName << endl;
    }
    return 0;
}
