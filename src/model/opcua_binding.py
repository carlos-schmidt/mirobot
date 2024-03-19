class OpcUABinding:
    def __init__(self, url, node, value, routine, poll_rate, req_timeout) -> None:
        self.__url = url
        self.__node = node
        self.__value = value
        self.__routine = routine
        self.__poll_rate = poll_rate
        self.__req_timeout = req_timeout

    def get(self):
        return (
            self.__url,
            self.__node,
            self.__value,
            self.__routine,
            self.__poll_rate,
            self.__req_timeout,
        )

    def get_url(self):
        return self.__url
    
    def get_routine(self):
        return self.__routine
    
    def get_rate(self) -> float:
        return float(self.__poll_rate)
    
    def get_node(self):
        return self.__node
    
    def get_value(self):
        return self.__value