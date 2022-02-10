import cluster

def main():
    print("main is running")
    cluster1 = cluster.Cluster()
    
    # demo data
    demoTuple = ("Tim", 21, "Computer Science", "M")
    cluster1.add_to_cluster(demoTuple)
    print("ranges: " + str(cluster1.ranges))
    demoTuple = ("Callum", 20, "Computer Science", "M")
    cluster1.add_to_cluster(demoTuple)
    print("ranges: " + str(cluster1.ranges))
    demoTuple = ("Xindi", 21, "Data Science", "F")
    cluster1.add_to_cluster(demoTuple)
    print("ranges: " + str(cluster1.ranges))
    demoTuple = ("Jeremie", 22, "Discrete Maths", "M")
    cluster1.add_to_cluster(demoTuple)
    print("ranges: " + str(cluster1.ranges))

    print(cluster1.tuples)
    cluster_size = cluster1.__len__()
    print("cluster size: " + str(cluster_size))
    

if __name__ == "__main__":
    main()