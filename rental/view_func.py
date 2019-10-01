def quadrant_format(df):
    # Conditionally replace quadrant names
    df.loc[df["quadrant"] == "", "quadrant"] = "Unspecified"
    df.loc[
        (df["quadrant"] == "Inner-City||SW") | (df["quadrant"] == "SW||Inner-City"),
        "quadrant",
    ] = "SW-Central"
    df.loc[
        (df["quadrant"] == "Inner-City||NW") | (df["quadrant"] == "NW||Inner-City"),
        "quadrant",
    ] = "NW-Central"
    df.loc[
        (df["quadrant"] == "Inner-City||SE") | (df["quadrant"] == "SE||Inner-City"),
        "quadrant",
    ] = "SE-Central"
    df.loc[
        (df["quadrant"] == "Inner-City||NE") | (df["quadrant"] == "NE||Inner-City"),
        "quadrant",
    ] = "NE-Central"

    return df


if __name__ == "__main__":
    print("main")
