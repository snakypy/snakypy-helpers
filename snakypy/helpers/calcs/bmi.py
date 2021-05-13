class BMI:
    """Class that will calculate the body mass index."""

    def __init__(self, sex: str, weight: float, height: float):
        self.sex = sex.lower()
        self.weight = weight
        self.height = height
        self.register_male = {"V1": 20.7, "V2": 26.4, "V3": 27.8, "V4": 31.1}
        self.register_female = {"V1": 19.1, "V2": 25.8, "V3": 27.3, "V4": 32.3}

    def calc_bmi(self) -> float:
        """
        This method will perform the body mass index calculation.
        Applied within the "calc_bmi" method.
        """
        try:
            w: float = self.validate_hw(self.weight, 0, 350)
            h: float = self.validate_hw(self.height, 0, 3)
            return w / (h * h)
        except Exception:
            raise

    def validate_sex(self) -> str:
        """Method to validate the person's gender."""
        if self.sex != "m" and self.sex != "f":
            raise AttributeError("Error entering gender type. Use M or F.")
        return self.sex

    @staticmethod
    def validate_hw(hw: float, value1: float, value2: float) -> float:
        """
        This is a static method for validating weight and height.
        The height cannot be greater than 3 meters and neither the weight
        above 350, nor can both be zeroed or negative
        """
        if hw <= value1 or hw > value2:
            if hw < 0:
                raise AttributeError("Error Attribute")
        return hw

    @staticmethod
    def reply(result_bmi: float, reg: dict) -> str:
        """
        The purpose of this statistical method is to receive the calculation
        of the body mass index already done, and to compare it with the
        statistical data informed in the initializer method of the class.
        """
        if result_bmi < reg["V1"]:
            return "Under weight."
        elif reg["V1"] <= result_bmi < reg["V2"]:
            return "Normal weight."
        elif reg["V2"] <= result_bmi < reg["V3"]:
            return "Marginally overweight."
        elif reg["V3"] <= result_bmi < reg["V4"]:
            return "Overweight."
        elif result_bmi > reg["V4"]:
            return "Obesity."
        else:
            raise AttributeError("Error Attribute")

    def main(self) -> str:
        if self.calc_bmi():
            if self.validate_sex() == "m":
                return self.reply(self.calc_bmi(), self.register_male)
            elif self.validate_sex() == "f":
                return self.reply(self.calc_bmi(), self.register_female)
        raise


def bmi(sex: str, weight: float, height: float) -> str:
    """
    This function is responsible for calling the class of body mass index (BMI).

    >>> from snakypy.helpers.calcs import bmi
    >>> bmi('m', 60, 1.73)
    'Under weight.'

    Args:
        sex (str): You must receive a string with a single character.
             The string must be either "m" for "male" or "f" for "female"

        weight (float): You should receive a float, this is where you put the weight

        height (float): You should receive a float, this is where you put the height

    Returns:
        The return will be a string informing the result or a false Boolean, if the arguments are wrong.
    """

    return BMI(sex, weight, height).main()


__all__ = ["bmi"]
