class singleton(type):
    """
    usage:
    ```
    __metaclass__ = singleton
    ```
    """

    def __init__(cls, name, bases, dict):  # pylint: disable=W0622
        super(singleton, cls).__init__(name, bases, dict)
        cls.instance = None

    def __call__(cls, *args, **kw):
        if cls.instance is None:
            cls.instance = super(singleton, cls).__call__(*args, **kw)
        return cls.instance
