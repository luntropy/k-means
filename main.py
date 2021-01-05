#!/usr/bin/python3

from copy import deepcopy
import matplotlib.pyplot as plt
import math
import re
import random

color_pallet = [ 'r', 'g', 'b', 'c', 'm', 'gold', 'darkorange', 'springgreen', 'steelblue', 'navy', 'indigo', 'lightcoral', 'deepskyblue' ]

class Point:
    def __init__(self):
        self.id = None
        self.x = None
        self.y = None
        self.color = None
        self.cost = None

    def __init__(self, id, x, y, color, cost):
        self.id = id
        self.x = x
        self.y = y
        self.color = color
        self.cost = cost

    def eq_point(self, point):
        if self.x == point.x and self.y == point.y:
            return True

        return False

def prepare_data(data):
    data_adj = []

    for vect in data:
        if '\t' in vect:
            vect = vect.replace('\t', ' ')

        data_adj.append(vect)

    data_split = []
    for element in data_adj:
        data_split.append(re.split(r' +', element))

    data_prepared = []
    for element in data_split:
        temp = []
        temp.append(float(element[0]))
        temp.append(float(element[1]))

        data_prepared.append(temp)

    return data_prepared

def create_points(data):
    points = []

    iter = 0
    for coordinates in data:
        p = Point(iter, round(coordinates[0], 3), round(coordinates[1], 3), 'k', 0)
        points.append(p)

        iter = iter + 1

    return points

def choose_centroids(points, N):
    random.shuffle(points)

    centroids = []
    for i in range(0, N):
        centroid = Point(-1, points[i].x, points[i].y, color_pallet[i], 0)
        centroids.append(centroid)

    return centroids

def calc_distance(point, centroid):
    return round(math.sqrt(math.pow(point.x - centroid.x, 2) + math.pow(point.y - centroid.y, 2)), 3)

def min_distance_color(point, centroids):
    min_dist = float('inf')
    best_centroid = None

    for i in centroids:
        dist = calc_distance(point, i)

        if dist < min_dist:
            min_dist = dist
            best_centroid = i

    return (best_centroid.color, min_dist)

def assign_clusters(points, centroids):
    clusters = {}
    clusters['changed'] = 'No'
    clusters['total_cost'] = 0

    total_cost = 0
    for point in points:
        res = min_distance_color(point, centroids)
        color_assign = res[0]
        cost_assign = res[1]

        point.cost = cost_assign
        total_cost = total_cost + point.cost
        if point.color != color_assign:
            point.color = color_assign
            clusters['changed'] = 'Yes'

        if color_assign not in clusters.keys():
            clusters[color_assign] = []

        clusters[color_assign].append(point)

    clusters['total_cost'] = total_cost

    return clusters

def calc_mean(cluster):
    points = len(cluster)
    x_mean = 0
    y_mean = 0

    for point in cluster:
        x_mean = x_mean + point.x
        y_mean = y_mean + point.y

    return (round(x_mean / points, 3), round(y_mean / points, 3))

def update_centroids(clusters, centroids, generation):
    new_centroids = []

    for cluster in clusters.keys():
        if cluster != 'changed' and cluster != 'total_cost':
            centroid_coordinates = calc_mean(clusters[cluster])

            new_centroid = Point(generation, centroid_coordinates[0], centroid_coordinates[1], cluster, 0)
            new_centroids.append(new_centroid)

    return new_centroids

def plot(clusters, centroids):
    for cluster in clusters.keys():
        if cluster != 'changed' and cluster != 'total_cost':
            for point in clusters[cluster]:
                plt.scatter(point.x, point.y, color = point.color, zorder = -1)

    for centroid in centroids:
        plt.scatter(centroid.x, centroid.y, marker = 'x', color = 'k', zorder = 1)

    plt.show()
    plt.clf()

def find_clusters(points, N):
    centroids = choose_centroids(points, N)
    clusters = assign_clusters(points, centroids)

    generation = -2
    iter = 0
    while iter < 100:
        new_centroids = update_centroids(clusters, centroids, generation)

        new_clusters = assign_clusters(points, new_centroids)

        if new_clusters['changed'] == 'No':
            break

        clusters = new_clusters
        centroids = new_centroids

        generation = generation - 1
        iter = iter + 1

    return (clusters, centroids)

def solution(data_prep, N):
    points = create_points(data_prep)
    min_cost = float('inf')
    best_iter = 0

    iter = 0
    clusters = None
    while iter <= 50:
        temp = find_clusters(points, N)
        print('{0}: {1}'.format(iter, temp[0]['total_cost']))

        if temp[0]['total_cost'] < min_cost:
            best_iter = iter
            min_cost = temp[0]['total_cost']
            clusters = deepcopy(temp)

        iter = iter + 1

    print('Best {0}: {1}'.format(best_iter, clusters[0]['total_cost']))
    plot(clusters[0], clusters[1])

if __name__ == '__main__':
    file_name = input('File name: ')
    N = int(input('Clusters: '))

    with open('./data/{0}/{0}.txt'.format(file_name), 'r') as data_file:
        data = data_file.read().splitlines()

    data_prep = prepare_data(data)

    solution(data_prep, N)
