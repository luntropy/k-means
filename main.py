#!/usr/bin/python3

import matplotlib.pyplot as plt
import re
import math
import random

color_pallet = [ 'r', 'g', 'b', 'c', 'm', 'gold', 'darkorange', 'springgreen', 'steelblue', 'navy', 'indigo', 'lightcoral', 'deepskyblue' ]

class Point:
    def __init__(self):
        self.id = None
        self.x = None
        self.y = None
        self.color = None

    def __init__(self, id, x, y, color):
        self.id = id
        self.x = x
        self.y = y
        self.color = color

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
        p = Point(iter, round(coordinates[0], 3), round(coordinates[1], 3), 'k')
        points.append(p)

        iter = iter + 1

    return points

def choose_centroids(points, N):
    positions = []
    for i in range(0, N):
        pos = random.randrange(0, len(points))
        positions.append(pos)

    centroids = []
    for i in range(0, N):
        points[positions[i]].color = color_pallet[i]

        centroid = Point(-1, points[positions[i]].x, points[positions[i]].y, color_pallet[i])
        centroids.append(centroid)

    return centroids

def calc_distance(point, centroid):
    return round(math.sqrt(math.pow(point.x - centroid.x, 2) + math.pow(point.y - centroid.y, 2)), 3)

def min_distance_color(point, centroids):
    max_dist = float('inf')
    best_centroid = None

    for i in centroids:
        dist = calc_distance(point, i)

        if dist < max_dist:
            max_dist = dist
            best_centroid = i

    return best_centroid.color

def assign_clusters(points, centroids):
    clusters = {}
    clusters['changed'] = 'No'

    for point in points:
        color_assign = min_distance_color(point, centroids)

        if point.color != color_assign:
            point.color = color_assign
            clusters['changed'] = 'Yes'

        if color_assign not in clusters.keys():
            clusters[color_assign] = []

        clusters[color_assign].append(point)

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

    for centroid in centroids:
        centroid_coordinates = calc_mean(clusters[centroid.color])

        new_centroid = Point(generation, centroid_coordinates[0], centroid_coordinates[1], centroid.color)
        new_centroids.append(new_centroid)

    return new_centroids

def plot(clusters):
    for cluster in clusters.keys():
        if cluster != 'changed':
            for point in clusters[cluster]:
                plt.scatter(point.x, point.y, color = point.color)

    plt.show()

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

        generation = generation - 1
        iter = iter + 1

    plot(clusters)

if __name__ == '__main__':
    # with open('./data/normal/normal.txt', 'r') as data_file:
    #     data = data_file.read().splitlines()

    with open('./data/unbalance/unbalance.txt', 'r') as data_file:
        data = data_file.read().splitlines()

    data_prep = prepare_data(data)
    points = create_points(data_prep)

    N = int(input())
    find_clusters(points, N)
