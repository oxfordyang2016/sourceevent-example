#!/usr/bin/env python
import itertools
import time
from flask import Flask, Response, redirect, request, url_for
import redis
# solution
#https://stackoverflow.com/questions/13386681/streaming-data-with-python-and-flask


app = Flask(__name__)
r = redis.StrictRedis(host='localhost', port=6379)  
p = r.pubsub()  
p.subscribe('channel_1') 
                        # Connect to local Redis instance

@app.route('/')
def index():
    # 客户端过来的请求如果头部包含的数据里面含有这个返回如下的服务器推送数据
    if request.headers.get('accept') == 'text/event-stream':

        def events():
            a  = 3
            b= 2
            # 这里是向前端不断传送数据的部分
            yield "data: %s \n\n" % ("顶尖的伟业需要艰苦卓绝的奋斗")
            for i, c in enumerate(itertools.cycle('\|/-')):
                time.sleep(1)
                message = p.get_message()
                print(message)
                print(b,a)
                if message != None:
                    try:
                        print(message["data"])
                        time.sleep(0.2)
                        yield "data: %.3f\n\n" % (float(message["data"]))
                    except:
                        print("datat get error")
                else:
                    print("检测是否执行下一句")
                a = a*-1
                
                print("---------------")
                # time.sleep(10)  # an artificial delay
        return Response(events(), content_type='text/event-stream')
    return redirect(url_for('static', filename='score.html'))

if __name__ == "__main__":
    app.run(host='localhost', port=234)
