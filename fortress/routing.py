# coding: utf-8
__author__ = "HanQian"

# routing.py文件其实就是个表单，功能和Django原来的urls.py文件一样，
# 不过这里使用的不是URL，而是请求的类型。

from channels.routing import route,route_class
from fortress.consumers import Webterminal,TerminalMonitor
channel_routing = [
    route_class(Webterminal),
    # route_class(CommandExecute,path= r'^/execute'),
    route_class(TerminalMonitor,path= r'^/monitor/(?P<channel>\w+-\w+-\w+-\w+-\w+-\w+)'),
]
