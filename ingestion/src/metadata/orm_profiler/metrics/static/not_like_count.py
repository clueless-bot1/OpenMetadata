#  Copyright 2021 Collate
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#  http://www.apache.org/licenses/LICENSE-2.0
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

"""
Like Count Metric definition
"""
# pylint: disable=duplicate-code

from sqlalchemy import case, column, func

from metadata.orm_profiler.metrics.core import StaticMetric, _label


class NotLikeCount(StaticMetric):
    """
    NOT_LIKE_COUNT Metric

    Given a column, and an expression, return the number of
    rows that match the forbidden regex pattern

    This Metric needs to be initialised passing the expression to check
    add_props(expression="j%")(Metrics.NOT_LIKE_COUNT.value)
    """

    expression: str

    @classmethod
    def name(cls):
        return "notLikeCount"

    @property
    def metric_type(self):
        return int

    @_label
    def fn(self):
        if not hasattr(self, "expression"):
            raise AttributeError(
                "Not Like Count requires an expression to be set: add_props(expression=...)(Metrics.NOT_LIKE_COUNT)"
            )
        return func.sum(
            case([(column(self.col.name).not_like(self.expression), 0)], else_=1)
        )
