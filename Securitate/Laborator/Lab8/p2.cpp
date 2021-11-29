#include <iostream>
#include <string.h>
using namespace std;
int main()
{
 	char input[7];
 	char pass[7] = "fmiSSI";
 	int passLen = strlen(pass);
 	cout<<"Introduceti parola: ";
 	cin>>input;
 	if (strncmp(input,pass,passLen)==0) {
 		cout<<"Parola introdusa este corecta!\n";
 	}
 	else {
 		cout<<"Ati introdus o parola gresita :(\n";
 	}
 	return 0;
}
