class XshSession:
    __ip = ""
    __port = ""
    __username = ""
    __password = ""
    __protocol = ""
    __prompt = ""
    __default_prompt = {"ssh": "]$ ", "telnet": "", "sftp": "", "ftp": ""}
    __url = ""
    __tab_name = ""

    @staticmethod
    def MsgBox(msg_str: str):
        return xsh.Dialog.MsgBox(msg_str)

    @staticmethod
    def MessageBox(lpszMessage: str, lpszTitle: str, nType: int):
        return xsh.Dialog.MessageBox(lpszMessage, lpszTitle, nType)

    @staticmethod
    def Prompt(lpszMessage: str, lpszTitle: str, lpszDefault: str, bHidden: bool):
        return xsh.Dialog.Prompt(lpszMessage, lpszTitle, lpszDefault, bHidden)


    def __init__(self, ip, port="22", username="", password="", protocol="ssh", prompt="NA"):
        self.__ip = ip
        self.__port = port
        self.__username = username
        self.__password = password
        self.__protocol = protocol
        self.__tab_name = ip + ":" + port
        if protocol not in self.__default_prompt:
            raise Exception("Protocol Not Supported: " + protocol)
        if prompt == "NA":
            self.__prompt = self.__default_prompt[protocol]
        else:
            self.__prompt = prompt
        self.__gen_url()

    def __gen_url(self):
        self.__url = self.__protocol + "://"
        if self.__username != "":
            self.__url += self.__username
            if self.__password != "":
                self.__url += ":" + self.__password
            self.__url += "@"
        self.__url += self.__ip + ":" + self.__port

    def open(self, timeout=30000):
        xsh.Session.Open(self.__url)
        while not xsh.Session.Connected:
            timeout -= 100
            xsh.Session.Sleep(100)
            if timeout <= 0:
                raise Exception("Connect Failed: " + self.__url)
        xsh.Session.Sleep(1000)
        return self

    def try_open(self, timeout=600000, retry_time=30000):
        xsh.Session.Open(self.__url)
        xsh.Session.Sleep(retry_time)
        while not xsh.Session.Connected:
            timeout -= retry_time
            if timeout <= 0:
                raise Exception("Connect Failed: " + self.__url)
            xsh.Session.Open(self.__url)
            xsh.Session.Sleep(retry_time)
        xsh.Session.Sleep(1000)
        return self

    def close(self, timeout=30000):
        xsh.Session.SelectTabName(self.__tab_name)
        xsh.Session.Close()
        while xsh.Session.Connected:
            timeout -= 100
            xsh.Session.Sleep(100)
            if timeout <= 0:
                raise Exception("Disconnect Failed: " + self.__url)
        xsh.Session.Sleep(1000)
        return self

    def send(self, cmd):
        xsh.Session.SelectTabName(self.__tab_name)
        xsh.Screen.Send(cmd + "\r")
        return self

    def do(self, cmd):
        if self.__prompt == "":
            return self.send(cmd)
        xsh.Session.SelectTabName(self.__tab_name)
        xsh.Screen.Send(cmd + "\r")
        xsh.Screen.WaitForString(self.__prompt)
        return self

    def wait(self, str):
        xsh.Session.SelectTabName(self.__tab_name)
        xsh.Screen.WaitForString(str)
        return self

    def sleep(self, time):
        xsh.Session.SelectTabName(self.__tab_name)
        xsh.Session.Sleep(time)
        return self

    def cd(self, path):
        self.do("cd " + path)
        return self

    def cp(self, source_path, dest_path):
        self.do("\\cp -f " + source_path + " " + dest_path)
        return self

    def get(self, filename):
        self.do("get " + filename)
        return self

    def put(self, filename):
        self.do("put " + filename)
        return self


def Main():
    telnet = XshSession("localhost", "1200", protocol="telnet", prompt="-> ")
    host = XshSession("localhost", "1201", protocol="telnet", prompt="-> ")
    file_server = XshSession("localhost", "1202", protocol="telnet", prompt="-> ")
    file_client = XshSession("localhost", "1203", protocol="telnet", prompt="-> ")
    update_server = XshSession("localhost", "1204", protocol="telnet", prompt="-> ")

    telnet.open() \
        .send("hello").wait("llo").sleep(1000) \
        .do("world") \
        .do("!!!") \
        .close()

    host.open() \
        .cd("/home/wishx") \
        .do("ls") \
        .send("cp file1.txt file_copy_1.txt").wait("(y/n)").do("y") \
        .cp("file2.txt", "file_copy_2.txt") \
        .do("pwd") \
        .close()

    file_server.open() \
        .cd("/home/wishx/output/") \
        .get("result_1.bin").sleep(500)
    file_client.open() \
        .cd("/home/wishx/update/") \
        .put("result_1.bin").sleep(500)
    file_server.get("result_2.bin").sleep(500)
    file_client.put("result_2.bin").sleep(500)
    file_server.get("result_3.bin").sleep(500)
    file_client.put("result_3.bin").sleep(500)
    file_server.get("result_4.bin").sleep(500)
    file_client.put("result_5.bin").sleep(500)
    file_server.close()
    file_client.close()

    update_server.open() \
        .do("update") \
        .send("update").wait("Update success!") \
        .close()
    XshSession.MsgBox("update success!")




