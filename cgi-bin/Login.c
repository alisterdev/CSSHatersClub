/*
 * COMP 206 Assignment 4
 * Alex I.
 * Manages registration on the website
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h> 

/*
 * Returns 0 if user/pass combination is correct,
 * 1 otherwise.
 */
int isValidUser(char *username, char *password) 
{

	FILE *filePointer;
	filePointer = fopen("members.csv", "rt");
    
    if (filePointer == NULL) {
        printf("Could not open the file! Try again!\n");
    } else {
        
        char line[1024];    
    	char delimiters[] = " ";
    	char user[256];
    	char pass[256];
    	
    	while (fscanf(filePointer, "%s", user) != EOF) {
    		if (strcmp(username, user) == 0) {
    			fscanf(filePointer, "%s", pass);
    			if (strcmp(password, pass) == 0) {
    				return 0;
    			}
    		}
    	}

        fclose(filePointer);
    }

	return 1;
}

int main(int argc, const char * argv[])
{
	char queryString[200];
	char c;
	int counter = 0;
	int queryLength = atoi(getenv("CONTENT_LENGTH"));
	char username[50];
	char password[50];

	printf("Content-Type:text/html\n\n");
	printf("<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'><title>Home | CSS Haters Club</title></head><body bgcolor='#0070e0'><font size='5' color='white' face='Helvetica Neue, Arial'><table align='center'>");	
	
	// read from stdin char by char, replace plus signs encodings in strings by spaces
	// and save new modified string into queryString variable
	while ((c = getchar()) != EOF && counter < queryLength) {
		if (counter < 200) {	
			if (c != '+') 
				queryString[counter] = c;
			 else 
			 	queryString[counter] = ' ';
			counter++;
		}
	}
	queryString[counter] = '\0';

	char delimiters[] = "&";
	char* str = strtok(queryString, delimiters);
	sscanf(str, "username=%s", username);
	str = strtok(NULL, delimiters);
	sscanf(str, "password=%s", password);
	int validUser = isValidUser(username, password);
	
	if (!validUser) {
		printf("<tr><td align='center'><br/><br/><br/><br/><br/><br/><br/><br/>Login successful!<br/></td></tr><tr><td align='center'>You will be redirected in 3 seconds...</td></tr>");
		printf("<meta http-equiv='refresh' content='3; url=http://cs.mcgill.ca/~ailea/comp206a4/cgi-bin/MyFacebookPage.py?username=%s'/>", username);
	} else {
		printf("<tr><td align='center'><br/><br/><br/><br/><br/><br/><br/><br/>Login failed!<br/></td></tr><tr><td align='center'>Please return to the <a href='../index.html'><font color='white'>login page</font></a> and try again!</td></tr>");		
	}

	printf("</table></font></body></html>");	

	return 0;
}