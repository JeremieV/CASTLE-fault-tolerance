from cluster import Cluster
from tuple_obj import TupleObj
    
def test_cluster():
    cluster1 = Cluster(("Name", "Age", "Course", "Sex"))
    tuple1 = TupleObj(("Tim", 21, "Computer Science", "M"), ("Name", "Age", "Course", "Sex"),  ("Age", "Sex"))
    cluster1.add_to_cluster(tuple1)
    print("ranges: " + str(cluster1.ranges))
    tuple2 = TupleObj(("Callum", 20, "Computer Science", "M"), ("Name", "Age", "Course", "Sex"),  ("Age", "Sex"))
    cluster1.add_to_cluster(tuple2)
    print("ranges: " + str(cluster1.ranges))
    tuple3 = TupleObj(("Xindi", 21, "Data Science", "F"), ("Name", "Age", "Course", "Sex"),  ("Age", "Sex"))
    cluster1.add_to_cluster(tuple3)
    print("ranges: " + str(cluster1.ranges))
    tuple4 = TupleObj(("Jeremie", 22, "Discrete Maths", "M"), ("Name", "Age", "Course", "Sex"),  ("Age", "Sex"))
    cluster1.add_to_cluster(tuple4)
    print("ranges: " + str(cluster1.ranges))

    gen_tuple = cluster1.get_generic(tuple1)
    gen_tuple.output_tuple()


if __name__ == "__main__":
    test_cluster()