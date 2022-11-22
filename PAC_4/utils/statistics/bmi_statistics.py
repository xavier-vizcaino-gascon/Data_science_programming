"""
Main tools for bmi statistics
"""
import pandas as pd


def calculate_bmi(df: pd.DataFrame, gender: str, year: int, cols_to_return: list) -> pd.DataFrame:
    """
    This function filters and subsets a dataframe and adds the column BMI

    param df: dataframe with information
    param gender: gender to filter data
    param year: year to filter data
    param cols_to_return: cols to be used as view and/or dataframe subset
    return: subset dataframe according to inputs + BMI column
    """
    def bmi_formula(row) -> float:
        """
        This function calculates bmi according to the formula

        param row: dataframe row
        return: returns bmi value
        """
        height = float(row["height_cm"] / 100)
        weight = float(row["weight_kg"])
        return weight / (height * height)

    # rows filter
    df = df[(df["gender"] == gender) & (df["year"] == year)]
    # create copy to avoid SettingWithCopyWarning
    df = df.copy()
    # BMI calculation
    df.loc[:, "BMI"] = df.apply(bmi_formula, axis=1)
    cols_to_return.append("BMI")
    # columns subset
    df = df.loc[:, cols_to_return]
    return df
