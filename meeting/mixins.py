from rest_framework import mixins


class QueryStringMixin:

    def get_query_params(self, keys):
        return {k: self.request.query_params.get(k) for k in keys}
