import datetime
import json
from os import listdir
from os.path import isfile, join

import pandas as pd
from django.db.models import F

from application.models import Branch, ServiceProvider, SPFrame, CustomerWaitingTime


def set_branch_service_providers(branch_name, indexes):
    branch = Branch.objects.get(name=branch_name)
    for index in indexes:
        x = ServiceProvider.objects.create(branch=branch, index=index)
        x.save()


def set_branch_names(name, category):
    Branch.objects.create(name=name, category=category)


def set_timeframe():
    current = datetime.datetime.now()
    start_time = current
    interval = datetime.timedelta(minutes=1)
    base_dir = "validation\\CoffeshopJS"
    services = ServiceProvider.objects.all()
    i = 0
    onlyfiles = [f for f in listdir(base_dir) if isfile(join(base_dir, f))]
    print(f"file sizes:{len(onlyfiles)}")
    step = int(len(onlyfiles) / 4)
    for service in services[:4]:
        onlyfiles = onlyfiles[i:i + step]
        for file in onlyfiles:
            # if len(file.split(".jpg"))>1:
            #     image = File(open(base_dir+index+"\\"+file,'rb'))
            head_coordinates = json.load(open(base_dir + "\\" + file))
            sp_frame = SPFrame.objects.create(creation_date=start_time, service_provider=service)
            start_time = start_time + interval
            sp_frame.head_coordinate = json.dumps(head_coordinates)
            sp_frame.save(update_fields=["head_coordinate"])
        start_time = current
        i += step


def calculate_waiting_time(service_provider_id):

    spframe = SPFrame.objects.filter(service_provider_id=service_provider_id).all()
    for i, sp in enumerate(spframe):
        customer_waiting_time_count = CustomerWaitingTime.objects.filter(service_provider_id=service_provider_id,
                                                                         updatable=True,x__gte=F("y")).count()
        frame_coordinate = json.loads(sp.head_coordinate)
        k = max(customer_waiting_time_count, len(list(frame_coordinate.keys())))
        if k>0:
            if customer_waiting_time_count == 0:
                for j in frame_coordinate.keys():
                    customer_waiting_time = CustomerWaitingTime.objects.create(start_date=i, last_updated=i,
                                                                               x=frame_coordinate[j][0],
                                                                               y=frame_coordinate[j][1],
                                                                               height=frame_coordinate[j][2],
                                                                               weight=frame_coordinate[j][3],
                                                                               service_provider_id=service_provider_id)
                    customer_waiting_time.save()
            elif len(list(frame_coordinate.keys())) ==0:
                for customer_waiting_time in CustomerWaitingTime.objects.filter(service_provider_id=service_provider_id, updatable=True):
                    customer_waiting_time.updatable = False
                    customer_waiting_time.save(update_fields=['updatable'])

            else:
                from sklearn.cluster import KMeans
                kmeans = KMeans(init="random", n_clusters=k, n_init=10, max_iter=300, random_state=42)
                df = pd.DataFrame(list(
                    CustomerWaitingTime.objects.filter(service_provider_id=service_provider_id, updatable=True).values()))
                current_state = df[['id', 'x', 'y', 'height', 'weight']]
                new_frame = [[0, i[0], i[1], i[2], i[3]] for i in frame_coordinate.values()]
                new_frame = pd.DataFrame(new_frame, columns=['id', 'x', 'y', 'height', 'weight'])
                if len(current_state) < len(new_frame):
                    kmeans.fit(new_frame[['x', 'y']].to_numpy())
                    current_state['label'] = kmeans.predict(current_state[['x', 'y']].to_numpy())
                    new_frame['label'] = kmeans.labels_
                else:
                    kmeans.fit(current_state[['x', 'y']].to_numpy())
                    new_frame['label'] = kmeans.predict(new_frame[['x', 'y']].to_numpy())
                    current_state['label'] = kmeans.labels_
                all_features = pd.concat([current_state, new_frame])
                for m, group in all_features.groupby(by='label'):
                    if len(group) == 2:
                        j = group[group['id'] == 0]
                        customer_waiting_time = CustomerWaitingTime.objects.get(id=group[group['id'] != 0]['id'].values[0])
                        customer_waiting_time.x = j['x']
                        customer_waiting_time.y = j['y']
                        customer_waiting_time.last_updated = i
                        customer_waiting_time.save(update_fields=['x', 'y', 'last_updated'])
                    if len(group) == 1:
                        if group['id'].values[0] == 0:
                            CustomerWaitingTime.objects.create(service_provider_id=service_provider_id,
                                                               x=group['x'].values[0], y=group['y'].values[0],
                                                               height=group['height'].values[0],
                                                               weight=group['weight'].values[0],start_date=i,last_updated=i)
                        else:
                            customer_waiting_time = CustomerWaitingTime.objects.get(id=group[group['id'] != 0]['id'].values[0])
                            customer_waiting_time.updatable = False
                            customer_waiting_time.save(update_fields=['updatable'])

