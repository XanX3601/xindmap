class Data:
    """A structure holding data.

    Attributes:
        text: data's text
    """
    def __init__(
        self,
        text=None
    ):
        """Instantiates self data.

        Args:
            text: data's text
        """
        self.text = '' if text is None else text

    def __eq__(self, other_data):
        """Tests wether self is equal to other_data

        self is equal to other_data if:
            - other_data is an instance of Data
            - self and other_data have the same text
        """
        if not isinstance(other_data, Data):
            return False

        return self.text == other_data.text

    def __str__(self):
        """Computes a string representation of data.

        Returns:
            A string representation of data.
        """
        return self.text

    def __repr__(self):
        """Computes a small string representation of data.

        Returns:
            A small string representation of data.
        """
        return str(self)
    
