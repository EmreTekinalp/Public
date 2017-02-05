#pragma once

#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <boost\algorithm\string.hpp>
using std::cin;
using std::cout;
using std::endl;
using std::ofstream;
using std::string;
using std::vector;


void getTextData(vector<string> &data)
{
    string alphabet = "abcdefghijklmnopqrstuvwxyz";
    boost::to_upper(alphabet);
    for (unsigned int i = 0; i < data.size(); i++)
    {
        data[i] = std::to_string(i) + ". This is a new line " + alphabet[i];
        cout << data[i] << endl;
    }
}


int main(int argc, char* argv[])
{
    ofstream outFile;
    string outFileName = "README.txt";

    vector<string> data(10);
    getTextData(data);

    outFile.open(outFileName);
    if (outFile.is_open())
    {
        for (auto d : data)
        {
            outFile << d << endl;
        }
        outFile.close();
    }
    else
    {
        cout << "Could not create file: " << outFileName << endl;
    }

    return 0;
}
