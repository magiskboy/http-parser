enum STATE {METHOD, URL, VERSION, HEADER, BODY};

struct parser_t {
    char token[4096];
    enum STATE state;

    // callback
    void (*on_method)(char*);
    void (*on_url)(char*);
    void (*on_http_version)(char*);
    void (*on_header)(char*, char*);
    void (*on_headers_completed)(void);
    void (*on_body)(char*);
};

static int pparser_parse_header(char*, char*, char*);

int pparser_parse(char*, struct parser_t*);
