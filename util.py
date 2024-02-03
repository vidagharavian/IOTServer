import json
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans


def json_to_feature(regions):
    all=[]
    for j in regions:
        if "shape_attributes" in j.keys():
            j= j["shape_attributes"]
        if 'updatable' not in j.keys() or j["updatable"]:
            row = [j['x'],j['y']]
            if "id" in j.keys():
                row.append(j["id"])
            else:
                row.append(0)
            all.append(row)
    return pd.DataFrame(all,columns=['x','y','id'])

def calculate_edlidician(a,b):
    return np.linalg.norm(a - b)

# def calculate_distance(current_state,given_frame):
#     for row in current_state:
#         for frame in given_frame:
#             row
def read_frame(frame):
    current_state = pd.DataFrame(columns=['x','y','start_frame','end_frame','id','updatable'])
    id =1
    for n in range(1,151):
        if n == 108:
            print(n)
        current_state = current_state[current_state['updatable'] == True]
        frame_coordinate = json.load(open(f"test_data/{frame}/{n:03}.json"))
        frame_coordinate = list(frame_coordinate.values())[0]
        k= max(len(current_state),len(frame_coordinate["regions"]))
        frame_name = int(frame_coordinate["filename"].split(".jpg")[0])
        if len(current_state)==0:
            current_frame =[]
            for j in frame_coordinate["regions"]:
                j=j["shape_attributes"]
                j["start_frame"] = frame_name
                j["end_frame"] = frame_name
                j["id"] =id
                j["updatable"] = True
                id+=1
                current ={}
                for key in ["x","y","start_frame","end_frame","id","updatable"]:
                    current[key]=j[key]
                current_frame.append(current)

            current_state = pd.DataFrame.from_records(current_frame)
        else:
            from sklearn.cluster import KMeans
            kmeans = KMeans(init="random", n_clusters=k, n_init=10, max_iter=300, random_state=42)
            features = json_to_feature(frame_coordinate["regions"])
            prediction = current_state[['x','y','id']]
            if len(features) >= len(prediction):
                kmeans.fit(features[['x','y']].to_numpy())
                prediction['label'] = kmeans.predict(prediction[['x','y']].to_numpy())
                features['label'] = kmeans.labels_
            else:
                kmeans.fit(prediction[['x','y']].to_numpy())
                features['label']= kmeans.predict(features[['x','y']].to_numpy())
                prediction['label'] = kmeans.labels_
            df = pd.concat([features,prediction])
            for m,group in df.groupby(by="label"):
                if len(group)==2:
                    i = group[group['id']!=0]
                    j = group[group['id'] == 0]
                    current_state['x'][current_state["id"]==i['id'].values[0]]=j["x"].values[0]
                    current_state['y'][current_state["id"] == i['id'].values[0]] = j["y"].values[0]
                    current_state["end_frame"][current_state["id"] == i['id'].values[0]] =frame_name
                elif len(group)==1:
                    if group['id'].values[0] ==0:
                        group["start_frame"] = frame_name
                        group["end_frame"] = frame_name
                        group["id"] = id
                        group["updatable"] = True
                        id += 1
                        current_state = pd.concat([current_state, group], ignore_index=True, sort=False)
                    else:
                        current_state['updatable'][current_state['id']==group['id'].values[0]]= False
                        current_state["end_frame"][current_state["id"] == group['id'].values[0]] = frame_name
        print(current_state.head())
        current_state.to_csv(f"output/{n:03}.csv")
    return current_state






read_frame(49)