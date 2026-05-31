from sqlalchemy.orm import Query


class CustomQuery(Query):
    def filter_if(self, condition: bool, *criteria):
        """
        Apply filter criteria to the query if the condition is True.

        :param condition: A boolean condition to check.
        :param criteria: The filter criteria to apply if the condition is True.
        :return: The query with the applied filter criteria if the condition is True, otherwise the original query.
        """
        if condition:
            return self.filter(*criteria)
        return self