import matplotlib.pyplot as plt
import time
import cv2
import numpy as np
import winsound
import os
from pylsl import StreamInlet, resolve_stream, resolve_byprop
from datetime import datetime
import time

session = 13
fsound = os.path.join(os.getcwd(), 'assets', 'beep-07a.wav')
task = np.array([0 for _ in range(25)] + [1 for _ in range(25)] + [2 for _ in range(25)])
print(task)
[np.random.shuffle(task) for _ in range(10)]
print(task)

box = (cv2.imread('DemoImage/box.png'))
box = cv2.resize(box, (800,600))
pen = (cv2.imread('DemoImage/pen.png'))
pen = cv2.resize(pen, (800,600))
done = (cv2.imread('DemoImage/done.png'))
done = cv2.resize(done, (800,600))

ready = (cv2.imread('DemoImage/ready.png'))
ready = cv2.resize(ready, (800,600))

blnk = (cv2.cvtColor(cv2.imread('DemoImage/blank.png'), cv2.COLOR_BGR2RGB))
blnk = cv2.resize(blnk, (800,600))

img_map = {
    0:blnk,
    1:box,
    2:pen
}

print("Recording starting at ", datetime.now())
cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

signal = []
label = []
times = []
print("resolving the inlet")
stream = resolve_byprop('type', 'EEG')
inlet = StreamInlet(stream[0])

while True:
    sample, time = inlet.pull_chunk()
    if len(sample) > 0:
        break
print('done')

for t in task:
    samples = []
    timestamps = []
    desc = []
    show_img = img_map[t]

    cv2.imshow("window", ready)
    cv2.waitKey(2000)
    inlet.pull_chunk()
    
    cv2.imshow("window", show_img)
    cv2.waitKey(4000)
    sample, timestamp = inlet.pull_chunk()
    samples += sample
    timestamp += timestamp
    l = [-1 for _ in range(len(sample))]
    desc += l
    winsound.PlaySound(fsound, winsound.SND_FILENAME | winsound.SND_ASYNC)
    cv2.imshow("window", blnk)
    cv2.waitKey(4000)
    sample, timestamp = inlet.pull_chunk()
    samples += sample
    timestamp += timestamp
    l = [t for _ in range(len(sample))]
    desc += l

    cv2.imshow("window", done)
    cv2.waitKey(4000)
    sample, timestamp = inlet.pull_chunk()
    samples += sample
    timestamp += timestamp
    l = [-2 for _ in range(len(sample))]
    desc += l

    #stoer the data
    signal += samples
    label += desc
    times += timestamps

signal = np.array(signal)
label = np.array(label)
times = np.array(times)

np.save(f'signal_session_{session}', signal)
np.save(f'label_session_{session}', label)
np.save(f'timestamps_session_{session}', timestamp)
    

    



