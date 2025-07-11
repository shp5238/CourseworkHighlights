/******************************************************************************
HW #1, COMP 280 
given a file, it should be able to count the lines, using SLOC

Author: Shreya Pasupuleti 
*******************************************************************************/

#include <stdio.h>
#include <stdbool.h>//knows what booleans are

//variable initializations
int sloc = 0; 
int lines = 0; 
int totalSloc = 0; 
int totalLines = 0; 

enum States {
    normal,          // Default state (regular code)
    inString,        // Inside a string literal `"..."` 
    escapeString,    // Inside a string, after an escape character `\"`
    inCharLit,       // Inside a character literal `'x'`
    escapeChar,      // Inside a char literal, after an escape character `\'`
    inComment,       // Just encountered `/`, need to determine type
    singleComment,   // Inside a single-line comment `// ...`
    inMultiComment,  // Inside a multi-line comment `/* ...`
    endMultiComment  // Saw `*` in a multi-line comment, checking if it ends `*/`
};


void handleStates(int c, enum States *state) {
    switch (*state) {
        case normal:
            if (c == ';') {
                sloc++;  // Increase SLOC count only in normal code
            } else if (c == '"') {
                *state = inString;
            } else if (c == '\'') {
                *state = inCharLit;
            } else if (c == '/') {
                *state = inComment;  // Possible comment (needs confirmation)
            }
            break;

        case inString:
            if (c == '\\') {
                *state = escapeString;  // Handle escape character inside string
            } else if (c == '"') {
                *state = normal;  // End of string
            }
            break;

        case escapeString:  
            *state = inString;  // Return to string after escaping
            break;

        case inCharLit:
            if (c == '\\') {
                *state = escapeChar;  // Handle escape inside char literal
            } else if (c == '\'') {
                *state = normal;  // End of char literal
            }
            break;

        case escapeChar:  
            *state = inCharLit;  // Return to char literal after escaping
            break;

        case inComment:
            if (c == '/') {
                *state = singleComment;  // Single-line comment
            } else if (c == '*') {
                *state = inMultiComment;  // Multi-line comment detected
            } else {
                *state = normal;  // Not actually a comment
            }
            break;

        case singleComment:
            if (c == '\n') {
                *state = normal;  // Newline ends single-line comment
            }
            break;

        case inMultiComment:
            if (c == '*') {
                *state = endMultiComment;  // Possible end of multi-line comment
            }
            break;

        case endMultiComment:
            if (c == '/') {
                *state = normal;  // End of multi-line comment
            } else if (c != '*') {  
                *state = inMultiComment;  // Stay in multi-line comment
            }
            break;
    }
}

void readFile(FILE *fp){ //process chars in file 
    enum States state = normal; //var init

    //for loop to process
    for (char c = getc(fp); c != EOF; c = getc(fp)){ //look through file by char
        if (c == '\n'){
            lines++; //increase physical lines by 1
        }
        handleStates(c, &state); //update the state accordingly. 
    }
    //add semicolons to SLOC count and numLines to physical line count
    totalSloc += sloc; 
    totalLines += lines; 
}

int main(int argc, const char * argv[]){ 
    if (argc == 1){//uses standard input when no files in command line
        readFile(stdin);
        lines ++; //accounts for lack of new line in input for first line
        printf("%3d %6d (stdin)\n", sloc, lines);
    }else{ //reads the command line parameters
        for (int i = 1; i< argc; i++){ //loop through files
            sloc = 0; 
            lines = 0; //reset sloc and lines each loop

            FILE *fp = fopen(argv[i], "r"); //open file
            
            if (fp == NULL){ //error if file DNE 
                perror("Could not open file.\n");
                return 1; //indicate error
            }

            readFile(fp); //process file
            printf("%3d %6d %s\n", sloc, lines, argv[i]);
            fclose(fp); //close file
        }
    }
    
    if (argc > 2){ //if more than one file, print the totals
        printf("%3d %6d Total\n", totalSloc, totalLines);
    }
    return 0;
}