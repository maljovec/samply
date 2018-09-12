#ifndef RUNUTILS_H
#define RUNUTILS_H

#include <string>
#include <map>
using namespace std;

#define QHULLCMD "~/tools/qhull/qdelaunay Qt Qz i < temp.qhull > temp.out"

void printArguments();
void addArgument(string name, string value, string description="");
//void addArgument(string name, int value);
//void addArgument(string name, float value);
void processArgs(int argc, char *argv[]);
float getArgFloat(string name);
string getArgString(string name);
int getArgInt(string name);


#endif
