#include "./pparser.h"
#include <stdio.h>
#include <time.h>

char *data =
    "GET /wp-content/uploads/2010/03/hello-kitty-darth-vader-pink.jpg "
    "HTTP/1.1\r\nHost: www.kittyhell.com\r\nUser-Agent: Mozilla/5.0 "
    "(Macintosh; U; Intel Mac OS X 10.6; ja-JP-mac; rv:1.9.2.3) Gecko/20100401 "
    "Firefox/3.6.3 Pathtraq/0.9\r\nAccept: "
    "text/html,application/xhtml+xml,application/xml;q=0.9,*/"
    "*;q=0.8\r\nAccept-Language: ja,en-us;q=0.7,en;q=0.3\r\nAccept-Encoding: "
    "gzip,deflate\r\nAccept-Charset: "
    "Shift_JIS,utf-8;q=0.7,*;q=0.7\r\nKeep-Alive: 115\r\nConnection: "
    "keep-alive\r\nCookie: wp_ozh_wsa_visits=2; "
    "wp_ozh_wsa_visit_lasttime=xxxxxxxxxx; "
    "__utma=xxxxxxxxx.xxxxxxxxxx.xxxxxxxxxx.xxxxxxxxxx.xxxxxxxxxx.x; "
    "__utmz=xxxxxxxxx.xxxxxxxxxx.x.x.utmccn=(referral)|utmcsr=reader.livedoor."
    "com|utmcct=/reader/|utmcmd=referral\r\n\r\n";

void on_method(char *method) { printf("Method: %s\n", method); }

void on_url(char *url) { printf("URL: %s\n", url); }

void on_http_version(char *version) { printf("Version: %s\n", version); }

void on_header(char *name, char *value) {
  printf("Header: %s => %s\n", name, value);
}

void on_headers_completed() { printf("Done parsing headers\n"); }

void on_body(char *body) { printf("Body: %s\n", body); }

int main() {
  struct parser_t parser;
  parser.on_method = &on_method;
  parser.on_url = &on_url;
  parser.on_http_version = &on_http_version;
  parser.on_header = &on_header;
  parser.on_headers_completed = &on_headers_completed;
  parser.on_body = &on_body;
  parser.state = METHOD;

  pparser_parse(data, &parser);

  return 0;
}
