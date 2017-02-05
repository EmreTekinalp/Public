#pragma once

#include <iostream>
using std::cin;
using std::cout;
using std::endl;


void basicErrorHandler(int num)
{
    // Basic custom error handler function
    if (num == 0)
    {
        throw "Wrong number bro";
    }
    else if (num == 1)
    {
        throw "Still wrong number bro";
    }
}

int main(int argc, char* argv[])
{
    try
    {
        basicErrorHandler(0);
    }
    catch (char const * e)
    {
        cout << "Error message: " << e << endl;
    }

    cout << "Program is still running..." << endl;

    return 0;
}
