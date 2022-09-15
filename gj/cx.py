import numpy
import os

path = "/home/pi/live"
def get_coin(user):
    gift_count = 0
    try:
        gift_count = numpy.load('../users/'+user+'.npy')
    except:
        gift_count = 0
    return gift_count
    
    
files = os.listdir(path+'/users')
i=1
for f in files: 
    name = f.replace(".npy","")
    count = get_coin(name)
    print(str(i)+"、"+name+":"+str(count))
    i=i+1