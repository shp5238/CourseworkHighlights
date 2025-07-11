/****************************************************************
HW #3, COMP 280
translate and manipulate information in a binary file.
don't do bit shifting and masking. Use bit fields.

Author: Shreya Pasupuleti
****************************************************************/

#include <stdio.h>
#include <string.h>
#define NUM_RECORDS 5
#define NAME_SIZE 5
#define MONTH_STR_SIZE 4

static const char* months[13] = {
    " ", "jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"
};

#pragma pack(push, 1)
typedef struct Misc {
    unsigned short id : 2;
    unsigned short category : 2;
    unsigned short engaged : 1;
    unsigned short reserved : 3;
} Misc;

typedef struct Time {
    unsigned short year : 7;
    unsigned short month : 4;
    unsigned short day : 5;
    unsigned short hour : 5;
    unsigned short minute : 6;
    unsigned short reserved_1 : 5;
    unsigned short second : 6;
    unsigned short reserved_2 : 10;
} Time;

typedef struct Track {
    float latitude;
    float longitude;
    short altitude;
    char name[NAME_SIZE];
    Misc misc;
    Time time_reported;
} Track;
#pragma pack(pop)

void read_data(Track* buffer, int count, const char* file_name) {
    FILE* file = fopen(file_name, "rb");
    Track current;
    for (int i = 0; i < count; ++i) {
        fread(&current, sizeof(Track), 1, file);
        buffer[i] = current;
        memset(&current, 0, sizeof(Track));  // Clear for next read
    }
    fclose(file);
}

void write_data(Track* buffer, int count) {
    

    for (int i = 0; i < count; ++i) {
        printf(
            "lat: %f lon: %f alt: %hd name: %.5s ",
            buffer[i].latitude, buffer[i].longitude, buffer[i].altitude, buffer[i].name
        );

        // Print the ID
        switch (buffer[i].misc.id) {
            case 0: printf("id: unknown "); break;
            case 1: printf("id: friend "); break;
            case 2: printf("id: foe "); break;
            case 3: printf("id: neutral "); break;
        }

        // Print the category
        switch (buffer[i].misc.category) {
            case 0: printf("cat: ship "); break;
            case 1: printf("cat: ground vehicle "); break;
            case 2: printf("cat: airplane "); break;
        }

        // Print engagement status
        if (buffer[i].misc.engaged) {
            printf("engaged ");
        }

        // Print the time
        printf(
            "reported: %hu/%.3s/%02hu %02hu:%02hu:%02hu\n",
            2000 + buffer[i].time_reported.year,
            months[buffer[i].time_reported.month],
            buffer[i].time_reported.day,
            buffer[i].time_reported.hour,
            buffer[i].time_reported.minute,
            buffer[i].time_reported.second
        );
    }
}

int main(int argc, char** argv) {
    if (argc == 1) {
        perror("No arguments provided\n");
        return 1;
    }

    Track tracks[NUM_RECORDS];
    memset(tracks, 0, sizeof(Track) * NUM_RECORDS);  // Initialize with zeros
    read_data(tracks, NUM_RECORDS, argv[1]);
    write_data(tracks, NUM_RECORDS);

    return 0;
}
