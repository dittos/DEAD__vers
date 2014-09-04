from werkzeug.exceptions import BadRequest


class MethodWrapper(object):
    def __init__(self, method):
        self.method = method
        self.argument_specs = []
        self.encode_funcs = []

    def __get__(self, instance, owner):
        def bound_method(*args, **kwargs):
            for spec in self.argument_specs:
                kwargs[spec.name] = spec.extract(instance.request)
            response = self.method(instance, *args, **kwargs)
            for encode_func in self.encode_funcs:
                response = encode_func(response)
            return response
        return bound_method

    def add_argument_spec(self, spec):
        self.argument_specs.append(spec)

    def decorate_encode_funcs(self, encode_funcs):
        self.encode_funcs.extend(encode_funcs)

    @classmethod
    def wrap(cls, method):
        if isinstance(method, cls):
            return method
        return cls(method)


class ArgumentSpec(object):
    def __init__(self, name, default=None, type=None, required=False):
        self.name = name
        self.default = default
        self.type = type
        self.required = required

    def __call__(self, method):
        method = MethodWrapper.wrap(method)
        method.add_argument_spec(self)
        return method

    def extract(self, request):
        value = self.get_mapping(request).get(self.name)
        if value is None:
            if self.required:
                raise BadRequest()
            return self.default
        if self.type:
            value = self.type(value)
        return value


class path_arg(ArgumentSpec):
    def get_mapping(self, request):
        return request.path_args


class query_arg(ArgumentSpec):
    def get_mapping(self, request):
        return request.args


class form_arg(ArgumentSpec):
    def get_mapping(self, request):
        return request.form


class respond_with(object):
    def __init__(self, *encode_funcs):
        self.encode_funcs = encode_funcs

    def __call__(self, method):
        method = MethodWrapper.wrap(method)
        method.decorate_encode_funcs(self.encode_funcs)
        return method