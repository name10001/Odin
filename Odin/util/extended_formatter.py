from string import Formatter


class ExtendedFormatter(Formatter):
    def convert_field(self, value, conversion):
        """
        Extend conversion symbol
        Following additional symbol has been added
        * l: convert to string and low case
        * u: convert to string and up case
        * c: convert to string and capitalise

        default are:
        * s: convert with str()
        * r: convert with repr()
        * a: convert with ascii()
        """

        if conversion == "u":
            return str(value).upper()
        elif conversion == "l":
            return str(value).lower()
        elif conversion == "c":
            return str(value).capitalize()

        return super().convert_field(value, conversion)


extended_formatter = ExtendedFormatter()
