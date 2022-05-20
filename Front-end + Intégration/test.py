from fastai.vision import *

def f():
    learner = load_learner('/Users/elliotcole/Documents/TSP/S2/dvp_info/site')
    print('model loaded!')

    img = open_image('/Users/elliotcole/Documents/TSP/S2/dvp_info/site/uploads/batiment.jpg')

    prediction,pred_idx,outputs = learner.predict(img)
    print(prediction.obj)
    return prediction.obj
f()
#a href="{{ url_for('solutions') }}"