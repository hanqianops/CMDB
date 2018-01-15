# coding: utf-8
__author__ = "HanQian"
# routing.py相当于新的urls.py，而consumers.py就相当于新的view.py。


from django.http import HttpResponse
from channels.handler import AsgiHandler
from fortress.interactive import interactive_shell,get_redis_instance,SshTerminalThread
import json
import paramiko
import socket
import time
from channels.generic.websockets import WebsocketConsumer
from channels import Group


class Webterminal(WebsocketConsumer):
    ssh = paramiko.SSHClient()
    http_user = True
    http_user_and_session = True
    channel_session = True
    channel_session_user = True

    def connect(self, message):
        self.message.reply_channel.send({"accept": True})
        # permission auth
        self.message.reply_channel.send({"text": json.dumps(['channel_name', self.message.reply_channel.name])},
                                        immediately=True)

    def disconnect(self, message):
        # close threading
        print("------- websocket stop -------------")
        self.closessh()
        self.message.reply_channel.send({"accept": False})

        # audit_log = SshLog.objects.get(user=User.objects.get(username=self.message.user),
        #                                channel=self.message.reply_channel.name)
        # audit_log.is_finished = True
        # audit_log.end_time = now()
        # audit_log.save()
        self.close()

    def queue(self):
        queue = get_redis_instance()
        channel = queue.pubsub()
        return queue

    def closessh(self):
        # close threading
        print("------- ssh stop -------------")
        self.queue().publish(self.message.reply_channel.name, json.dumps(['close']))

    def receive(self, text=None, bytes=None, **kwargs):
        print(text, '========= receive text ===============')
        try:
            if text:
                data = json.loads(text)
                begin_time = time.time()
                if data[0] == 'ip':
                    ip = data[1]
                    width = data[2]
                    height = data[3]
                    self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    # try:
                    #     data = ServerInfor.objects.get(ip=ip)
                    #     port = data.credential.port
                    #     method = data.credential.method
                    #     username = data.credential.username
                    #     audit_log = SshLog.objects.create(user=User.objects.get(username=self.message.user),
                    #                                       server=data, channel=self.message.reply_channel.name,
                    #                                       width=width, height=height)
                    #     audit_log.save()
                    #     if method == 'password':
                    #         password = "123.com" #data.credential.password
                    #     else:
                    #         key = data.credential.key
                    # except ObjectDoesNotExist:
                    #     self.message.reply_channel.send({"text": json.dumps(
                    #         ['stdout', '\033[1;3;31mConnect to server! Server ip doesn\'t exist!\033[0m'])},
                    #                                     immediately=True)
                    #     self.message.reply_channel.send({"accept": False})
                    try:
                        #if method == 'password':
                            #self.ssh.connect(ip, port=22, username=username, password=password, timeout=3)
                        self.ssh.connect(ip, port=22, username='root', password='123.com', timeout=3)
                        #else:
                         #   self.ssh.connect('10.240.1.103', port=22, username='root', password='123.com', timeout=3)
                            #self.ssh.connect(ip, port=port, username=username, key_filename=key, timeout=3)
                    except socket.timeout:
                        self.message.reply_channel.send(
                            {"text": json.dumps(['stdout', '\033[1;3;31mConnect to server time out\033[0m'])},
                            immediately=True)
                        self.message.reply_channel.send({"accept": False})
                        return
                    except Exception:
                        self.message.reply_channel.send(
                            {"text": json.dumps(['stdout', '\033[1;3;31mCan not connect to server\033[0m'])},
                            immediately=True)
                        self.message.reply_channel.send({"accept": False})
                        return

                    chan = self.ssh.invoke_shell(width=width, height=height, )

                    # open a new threading to handle ssh to avoid global variable bug
                    t1 = SshTerminalThread(self.message, chan)
                    t1.setDaemon = True
                    t1.start()
                    from django.utils.timezone import now
                    import os
                    directory_date_time = now()
                    # log_name = os.path.join('{0}-{1}-{2}'.format(directory_date_time.year, directory_date_time.month,
                    #                                              directory_date_time.day),
                    #                         '{0}.json'.format(audit_log.log))
                    interactive_shell(chan, self.message.reply_channel.name, log_name=None, width=width,
                                      height=height)

                elif data[0] in ['stdin', 'stdout']:
                    self.queue().publish(self.message.reply_channel.name, json.loads(text)[1])
                elif data[0] == u'set_size':
                    self.queue().publish(self.message.reply_channel.name, text)
                else:
                    self.message.reply_channel.send(
                        {"text": json.dumps(['stdout', '\033[1;3;31mfa xian wei zhi ming ling!\033[0m'])}, immediately=True)
            elif bytes:
                self.queue().publish(self.message.reply_channel.name, json.loads(bytes)[1])
        except socket.error:
            # audit_log = SshLog.objects.get(user=User.objects.get(username=self.message.user),
            #                                channel=self.message.reply_channel.name)
            # audit_log.is_finished = True
            # audit_log.end_time = now()
            # audit_log.save()
            self.closessh()
            self.close()
        except Exception as e:
            import traceback
            print(traceback.print_exc())
            self.closessh()
            self.close()

class TerminalMonitor(WebsocketConsumer):
    http_user = True
    http_user_and_session = True
    channel_session = True
    channel_session_user = True

    def connect(self, message, channel):
        self.message.reply_channel.send({"accept": True})
        # permission auth
        Group(channel).add(self.message.reply_channel.name)

    def disconnect(self, message, channel):
        Group(channel).discard(self.message.reply_channel.name)
        self.message.reply_channel.send({"accept": False})
        self.close()

    def receive(self, text=None, bytes=None, **kwargs):
        pass
