#ifndef PPARSER_H
#define PPARSER_H

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "./pparser.h"

// super fast because don't fucking care whitespace trailling
#define TRIM 0


int pparser_parse(char* request, struct parser_t* parser) {
    int idx = 0, i = 0;
    char hname[40], hvalue[8 * 1024], url[2000];
    int len_request = strlen(request);
    char* t = NULL;

    while (idx < len_request) {
        switch (parser->state) {
            case METHOD:
                t = strchr(request+idx, 32);
                if (t == NULL) {
                    strcat(parser->token, request + idx);
                }
                else {
                    i = (int)(t - (request + idx));
                    strncat(parser->token, request + idx, i);
                    parser->on_method(parser->token);
                    parser->token[0] = 0;
                    idx += i + 1;
                    parser->state = URL;
                } 
                break;

            case URL:
                t = strchr(request + idx, 32);
                if (t == NULL) {
                    parser->on_url(request + idx);
                }
                else {
                    i = (int)(t - (request + idx));
                    strncpy(url, request + idx, i);
                    parser->on_url(url);
                    idx += i + 1;
                    parser->state = VERSION;
                } 
                break;

            case VERSION:
                t = strchr(request + idx, 10);
                if (t == NULL) {
                    strcat(parser->token, request + idx);
                }
                else {
                    i = (int)(t - (request + idx));
                    strncat(parser->token, request + idx, i);
                    parser->on_http_version(parser->token);
                    parser->token[0] = 0;
                    idx += i + 1;
                    parser->state = HEADER;
                } 
                break;

            case HEADER:
                t = strchr(request+idx, 10);

                if (i == -1) {
                    strcat(parser->token, request + idx);
                }
                else {
                    i = (int)(t - (request + idx));
                    strncat(parser->token, request + idx, i);

                    if (parser->token[0] == 13) {
                        parser->state = BODY;
                        parser->on_headers_completed();
                    }
                    else {
                        pparser_parse_header(parser->token, hname, hvalue);
                        parser->on_header(hname, hvalue);
                        parser->token[0] = 0;
                    }

                    idx += i + 1;
                } 

                break;
            case BODY:
                parser->on_body(request + idx);
                break;
        }
    }

    return 0;
}

static int pparser_parse_header(char* str, char* name, char* value) {

    char* sep = strchr(str, ':');
    if (sep == NULL) {
        perror("Header is invalid");
        return 1;
    }

    strncpy(name, str, (int)(sep - str));
    strcpy(value, sep+1);

    if (TRIM) {
        int len = strlen(str);
        int i = 0, l = 0;
        while (i < len && str[i] == 32) ++i;
        while (i + l < len && str[i+l] != 32) ++l;
        strncpy(name, str + i, l-1);
        name[l-1] = 0;

        i = 0;
        while (i < (str - sep) && *(sep + i + 1) == 32) ++i;
        strcpy(value, sep + 1 + i);
    }

    return 0;
}

#endif
