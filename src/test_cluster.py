from cluster import Cluster
    
def test_cluster():
    cluster1 = Cluster(("Name", "Age", "Course", "Sex"))
    tuple1 = ("Tim", 21, "Computer Science", "M")
    cluster1.add_to_cluster(tuple1)
    print("ranges: " + str(cluster1.ranges))
    tuple2 = ("Callum", 20, "Computer Science", "M")
    cluster1.add_to_cluster(tuple2)
    print("ranges: " + str(cluster1.ranges))
    tuple3 = ("Xindi", 21, "Data Science", "F")
    cluster1.add_to_cluster(tuple3)
    print("ranges: " + str(cluster1.ranges))
    tuple4 = ("Jeremie", 22, "Discrete Maths", "M")
    cluster1.add_to_cluster(tuple4)
    print("ranges: " + str(cluster1.ranges))

    gen_tuple = cluster1.get_generic(tuple1)
    print(gen_tuple)


if __name__ == "__main__":
    test_cluster()