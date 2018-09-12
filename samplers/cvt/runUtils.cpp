#include "runUtils.h"
#include <vector>
#include <cstdlib>
#include <cstdio>

map<string,string> args;
vector<string> argNames;
vector<string> argDescriptions;

void printArguments() {
	for(unsigned int i=0;i<argNames.size();i++) {
	  printf("%s (%s) : %s \n", argNames[i].c_str(), getArgString(argNames[i]).c_str(), argDescriptions[i].c_str());
	}
}

void addArgument(string name, string defaultValue, string description) {
	if(args.find(name)==args.end()) {
		argNames.push_back(name);
		argDescriptions.push_back(description);
	}
	args[name] = defaultValue;
}

void processArgs(int argc, char *argv[]) {
	for(int i=0;i<argc;i++) {
		if(args.find(string(argv[i]))!=args.end()) {
			if(i+1<argc) {
				addArgument(string(argv[i]), string(argv[i+1]));
			}
		}
	}
}

float getArgFloat(string name) {
	return atof(args[name].c_str());
}

string getArgString(string name) {
	return args[name];
}

int getArgInt(string name) {
	return atoi(args[name].c_str());
}
