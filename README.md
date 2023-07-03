# HTTP Parser 

# Just for education

## How it works?

Program use callback pattern and it can parse data partially with any chunk size.

You create new parser and register callback what you want to serve.

Parser provides some callbacks such as:
- on_method
- on_url
- on_http_version
- on_header
- on_headers_completed
- on_body

```c
void on_method(char *method) {
    printf("Method: %s\n", method);
}

void on_url(char *url) { 
    printf("URL: %s\n", url);
}

void on_http_version(char *version) {
    printf("Version: %s\n", version);
}

void on_header(char *name, char *value) {
  printf("Header: %s => %s\n", name, value);
}

void on_headers_completed() {
    printf("Done parsing headers\n"); 
}

void on_body(char *body) {
    printf("Body: %s\n", body); 
}

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

```

#### Notice!!!

URL and body is parsed partially so callback can be called in many times.


```
$ make main
Method:GET
URL: /wp-content/uploads/2010/03/hello-kitty-darth-vader-pink.jpg
Version: HTTP/1.1
Header: Host =>  www.kittyhell.com
Header: User-Agent =>  Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; ja-JP-mac; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 Pathtraq/0.9
Header: Acceptgent =>  text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Header: Accept-Language =>  ja,en-us;q=0.7,en;q=0.3
Header: Accept-Encoding =>  gzip,deflate
Header: Accept-Charsetg =>  Shift_JIS,utf-8;q=0.7,*;q=0.7
Header: Keep-Aliversetg =>  115
Header: Connectionrsetg =>  keep-alive
Header: Cookietionrsetg =>  wp_ozh_wsa_visits=2; wp_ozh_wsa_visit_lasttime=xxxxxxxxxx; __utma=xxxxxxxxx.xxxxxxxxxx.xxxxxxxxxx.xxxxxxxxxx.xxxxxxxxxx.x; __utmz=xxxxxxxxx.xxxxxxxxxx.x.x.utmccn=(referral)|utmcsr=reader.livedoor.com|utmcct=/reader/|utmcmd=referral
```

## Benchmark

```bash
$ make benc
3765244.533806 req/s
```

#### Just fucking care trailling whitespace!!!


## What do we learn from it?

First, our parser must keep a segment data because of partial parsing. This data is only append new data until it's meaning completely like a header, a method or a http version. It is flushed when be emited to callback.

We accept it but we should limit size of header.

Let's imagine, our server must handle 1.000.000 requests per second and maximum of header can be 1mb so memory may be increased to (1.000.000 * 1) / 1024 ~ 1000gb


Second, performance can be dropped by removing trailling whitespace of headers. I knew that so can you improve it? Let's do it and create PR for me 🚀
