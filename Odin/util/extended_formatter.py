from string import Formatter


class ExtendedFormatter(Formatter):
    HTML_SAFE = (range(ord("a"), ord("z") + 1),
                 range(ord("A"), ord("Z") + 1),
                 range(ord("1"), ord("9") + 1),
                 (ord("_"), ord("-")))

    def convert_field(self, value, conversion):
        """
        Extend conversion symbol
        Following additional symbol has been added
        * l: convert to string and low case
        * u: convert to string and up case
        * c: convert to string and capitalise
        * h: removes all html unsafe characters
        * r: replace spaces with underscores

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
        elif conversion == "r":
            return str(value).replace(" ", "_")
        elif conversion == "h":
            value_safe = ""
            for character in str(value).replace(" ", "_"):
                # if character is a-z, A-Z, 1-9 or is _
                for i in self.HTML_SAFE:
                    if ord(character) not in i:
                        continue
                value_safe += character
            return value_safe

        return super().convert_field(value, conversion)


extended_formatter = ExtendedFormatter()
