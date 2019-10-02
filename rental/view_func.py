def quadrant_format(df):
    # Conditionally replace quadrant names
    df["quadrant"].fillna("Unspecified", inplace=True)
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
    df.loc[(df["quadrant"] == "SW||Out-of-Town"), "quadrant"] = "SW"

    return df


def query_slice(df, p_type, quadrant, community):
    if p_type != "all":
        df = df[(df["_type"] == p_type)]

    if quadrant != "all":
        df = df[(df["quadrant"] == quadrant)]

    if community != "all":
        df = df[(df["community"] == community)]

    return df


if __name__ == "__main__":
    print("main")
