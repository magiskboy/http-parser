# STATE
STATE_METHOD = 0
STATE_PATH = 1
STATE_HTTP_VERSION = 2
STATE_HEADER = 3
STATE_BODY = 4


class ParserBase:
    def __init__(self, protocol, trim=True):
        self.protocol = protocol
        self.current_token = b""
        self.current_state = STATE_METHOD
        self.trim = trim

    def parse_header(self, header: bytes) -> (bytes, bytes):
        idx = header.find(b":")
        if idx < 0:
            raise ValueError(f"Header {header} is invalid")
        name, value = header[:idx], header[idx+1:]
        return (name.strip(), value.strip()) if self.trim else (name, value)

    def feed_data(self, data: bytes):
        for c in data.decode("utf-8"):
            self.current_token += c
            
            if self.current_state == STATE_METHOD:
                if self.current_token.endswith(" "):
                    self.protocol.on_method(self.current_token[:-1])
                    self.current_token = ""
                    self.current_state = STATE_PATH
                continue

            if self.current_state == STATE_PATH:
                if self.current_token.endswith(" "):
                    self.protocol.on_path(self.current_token[:-1])
                    self.current_token = ""
                    self.current_state = STATE_HTTP_VERSION
                continue

            if self.current_state == STATE_HTTP_VERSION:
                if self.current_token.endswith("\r\n"):
                    self.protocol.on_http_version(self.current_token[:-2])
                    self.current_token = ""
                    self.current_state = STATE_HEADER
                continue

            if self.current_state == STATE_HEADER:
                if self.current_token.endswith("\r\n"):
                    header = self.current_token[:-2]
                    if header:
                        self.protocol.on_header(*self.parse_header(header))
                        self.current_token = ""
                        self.current_state = STATE_HEADER
                    else: # blank line
                        self.protocol.on_headers_completed()
                        self.current_token = ""
                        self.current_state = STATE_BODY
                continue

            if self.current_state == STATE_BODY:
                self.protocol.on_body(self.current_token)
                self.current_token = ""


class Parser(ParserBase):
    def __init__(self, protocol, trim=True):
        super().__init__(protocol, trim)
        self.current_token = b""

    def feed_data(self, data: bytes):
        idx = 0
        len_data = len(data)
        while idx < len_data:
            if self.current_state == STATE_METHOD:
                i = data.find(b" ", idx)
                if i == -1:
                    self.current_token += data[idx:]
                    break
                else:
                    self.current_token += data[idx:i]
                    self.protocol.on_method(self.current_token)
                    self.current_token = b""
                    idx = i + 1
                    self.current_state = STATE_PATH
                    continue

            if self.current_state == STATE_PATH:
                i = data.find(b" ", idx)
                if i == -1:
                    self.current_token += data[idx:]
                    break
                else:
                    self.current_token += data[idx:i]
                    self.protocol.on_path(self.current_token)
                    self.current_token = b""
                    idx = i + 1
                    self.current_state = STATE_HTTP_VERSION
                    continue

            if self.current_state == STATE_HTTP_VERSION:
                i = data.find(b"\n", idx)
                if i == -1:
                    self.current_token += data[idx:]
                    break
                else:
                    self.current_token += data[idx:i]
                    self.protocol.on_http_version(self.current_token[:-1])
                    self.current_token = b""
                    idx = i + 1
                    self.current_state = STATE_HEADER
                    continue

            if self.current_state == STATE_HEADER:
                i = data.find(b"\n", idx)
                if i == -1:
                    self.current_token += data[idx:]
                    break
                else:
                    self.current_token += data[idx:i]
                    if self.current_token == b"\r\n":
                        self.current_state = STATE_BODY
                        self.protocol.on_headers_completed()
                    else:
                        header = self.current_token[:-1]
                        if header:
                            self.protocol.on_header(*self.parse_header(header))
                            self.current_token = b""
                    idx = i + 1

            if self.current_state == STATE_BODY:
                self.protocol.on_body(data[idx:])
                break


class Protocol:
    def on_body(self, chunk):
        ...

    def on_path(self, path):
        ...

    def on_header(self, name, value):
        ...

    def on_method(self, method):
        ...

    def on_http_version(self, version):
        ...

    def on_headers_completed(self):
        ...


def main():
    import time
    data = b"GET /wp-content/uploads/2010/03/hello-kitty-darth-vader-pink.jpg HTTP/1.1\r\nHost: www.kittyhell.com\r\nUser-Agent: Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; ja-JP-mac; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 Pathtraq/0.9\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Language: ja,en-us;q=0.7,en;q=0.3\r\nAccept-Encoding: gzip,deflate\r\nAccept-Charset: Shift_JIS,utf-8;q=0.7,*;q=0.7\r\nKeep-Alive: 115\r\nConnection: keep-alive\r\nCookie: wp_ozh_wsa_visits=2; wp_ozh_wsa_visit_lasttime=xxxxxxxxxx; __utma=xxxxxxxxx.xxxxxxxxxx.xxxxxxxxxx.xxxxxxxxxx.xxxxxxxxxx.x; __utmz=xxxxxxxxx.xxxxxxxxxx.x.x.utmccn=(referral)|utmcsr=reader.livedoor.com|utmcct=/reader/|utmcmd=referral\r\n\r\n"
    n_iters = 1_000_000
    trim = True
    
    _start_time = time.perf_counter()
    for i in range(n_iters):
        protocol = Protocol()
        parser = Parser(protocol, trim)
        parser.feed_data(data)
    _end_time = time.perf_counter()
    print(f"{n_iters / (_end_time - _start_time)} req/s")


if __name__ == '__main__':
    main()
