class TupleObj:

    """ A single tuple that can be stored in a cluster.
        """

    def __init__(self, data, attribute_headers, qi_attributes):
        self.data = list(data)
        self.attribute_headers: list(str) = list(attribute_headers)
        # attribute headers you want to be anonymised
        self.qi_attributes: list(str) = qi_attributes

    def output_tuple(self):
        output_str = "{"
        for val, head in zip(self.data, self.attribute_headers):
            output_str = output_str + (head + ": " + str(val) + ", ")
        output_str = output_str + ("}")
        print(output_str)
