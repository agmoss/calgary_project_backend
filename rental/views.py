from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings  # For file paths

# For api data
from django.db import connections
from django.db.models import Count, Avg
from django.http import JsonResponse
from rental.models import RentalData
from django.core import serializers

import json
import pandas as pd
import numpy as np

import rental.view_func as vf


def time_series(request, quadrant="all", community="all", p_type="all", active=1):
    """ 
    Time series data on selection
    """

    community = community.replace("_", " ")

    if active == 1:

        df = pd.DataFrame(
            list(
                RentalData.objects.using("rental_data")
                .values("_type", "retrieval_date", "price", "quadrant", "community")
                .filter(position="active")
            )
        )

    else:

        df = pd.DataFrame(
            list(
                RentalData.objects.using("rental_data").values(
                    "_type", "retrieval_date", "price", "quadrant", "community"
                )
            )
        )

    # Remove properties that have 0 dollars rent
    df = df[df.price != 0]

    df.set_index("retrieval_date", inplace=True)

    df = df.sort_index()

    # Format quadrant names
    df = vf.quadrant_format(df)

    # Slice
    df = vf.query_slice(df, p_type, quadrant, community)

    df.drop(columns=["_type", "quadrant"], inplace=True)

    agg = df.groupby(df.index).mean()

    agg = agg.round()

    flat = agg.to_dict()

    return JsonResponse(flat, safe=False)


def price_metrics(
    request, fun, quadrant="all", community="all", p_type="all", active=1
):
    """ 
    Price stats on selection
    """

    try:

        community = community.replace("_", " ")

        if active == 1:

            df = pd.DataFrame(
                list(
                    RentalData.objects.using("rental_data")
                    .values("_type", "price", "quadrant", "community")
                    .filter(position="active")
                )
            )

        else:

            df = pd.DataFrame(
                list(
                    RentalData.objects.using("rental_data").values(
                        "_type", "price", "quadrant", "community"
                    )
                )
            )

        # Format quadrant names
        df = vf.quadrant_format(df)

        # Slice
        df = vf.query_slice(df, p_type, quadrant, community)

        # Remove properties that have 0 dollars rent
        df = df[df.price != 0]

        if fun == "avg":
            val = df["price"].mean()
        elif fun == "min":
            val = df["price"].min()
        elif fun == "max":
            val = df["price"].max()
        else:
            val = df["price"].mean()

        val = round(val)

        return JsonResponse(
            {
                "fun": fun,
                "quadrant": quadrant,
                "community": community,
                "p_type": p_type,
                "val": val,
            },
            safe=False,
        )

    except:

        return JsonResponse(
            {
                "fun": fun,
                "quadrant": quadrant,
                "community": community,
                "p_type": p_type,
                "val": 0,
            },
            safe=False,
        )


def listing_count(request, quadrant="all", community="all", p_type="all", active=1):
    """ 
    Count of rental listings for selection
    """

    try:

        community = community.replace("_", " ")

        if active == 1:

            df = pd.DataFrame(
                list(
                    RentalData.objects.using("rental_data")
                    .values("_type", "price", "quadrant", "community")
                    .filter(position="active")
                )
            )

        else:

            df = pd.DataFrame(
                list(
                    RentalData.objects.using("rental_data").values(
                        "_type", "price", "quadrant", "community"
                    )
                )
            )

        # Format quadrant names
        df = vf.quadrant_format(df)

        # Slice
        df = vf.query_slice(df, p_type, quadrant, community)

        val = df.shape[0]

        return JsonResponse(
            {"quadrant": quadrant, "community": community,
                "p_type": p_type, "count": val},
            safe=False,
        )

    except:

        return JsonResponse(
            {"quadrant": quadrant, "community": community,
                "p_type": p_type, "count": 0},
            safe=False,
        )


def market_share(request, quadrant="all", community="all", p_type="all", active=1):
    """ 
    Market cap of selection
    """

    try:

        community = community.replace("_", " ")

        if active == 1:

            df = pd.DataFrame(
                list(
                    RentalData.objects.using("rental_data")
                    .values("_type", "price", "quadrant", "community")
                    .filter(position="active")
                )
            )

        else:

            df = pd.DataFrame(
                list(
                    RentalData.objects.using("rental_data").values(
                        "_type", "price", "quadrant", "community"
                    )
                )
            )

        # Format quadrant names
        df = vf.quadrant_format(df)

        # Cache before slice
        df_total = df.copy()

        df = vf.query_slice(df, p_type, quadrant, community)

        val = df.shape[0] / df_total.shape[0]

        return JsonResponse(
            {
                "quadrant": quadrant,
                "p_type": p_type,
                "community": community,
                "val": df.shape[0],
                "total": df_total.shape[0],
                "ms": val,
            },
            safe=False,
        )

    except:

        return JsonResponse(
            {
                "quadrant": quadrant,
                "p_type": p_type,
                "community": community,
                "val": 0,
                "total": 0,
                "ms": 0,
            },
            safe=False,
        )


def scatter_data(request, quadrant="all", community="all", p_type="all", active=1):
    """ JSON API for scatter plot """

    community = community.replace("_", " ")

    if active == 1:

        df = pd.DataFrame(
            list(
                RentalData.objects.using("rental_data").values(
                    'community', 'quadrant', 'price', 'sq_feet', '_type'
                )
                .filter(position="active")
            )
        )

    else:

        df = pd.DataFrame(
            list(
                RentalData.objects.using("rental_data").values(
                    'community', 'quadrant', 'price', 'sq_feet', '_type'
                )
            )
        )

    # Format quadrant names
    df = vf.quadrant_format(df)

    # Slice
    df = vf.query_slice(df, p_type, quadrant, community)

    # We only need price/sq feet
    df.drop(columns=["_type", "quadrant","community"], inplace=True)

    # Remove properties that have 0 dollars rent
    df = df.loc[(df.price > 100) & (df.price <10000)]

    # Remove properties that have 0 dollars rent
    df = df.loc[(df.sq_feet > 100) & (df.sq_feet <10000)]

    df.sq_feet = df.sq_feet.astype(int)

    if df.shape[0] > 2500:
        df = df.sample(n=2500)

    flat = df.to_dict('split')

    return JsonResponse(flat["data"], safe=False)


def community_list(request):
    """ 
    Returns a list of signfigant communities
    """

    community = community.replace("_", " ")

    df = pd.DataFrame(
        list(
            RentalData.objects.using("rental_data")
            .values("community")
            .filter(position="active")
        )
    )

    df = df.community.value_counts()

    flat = df.to_dict()

    return JsonResponse({"resp": flat}, safe=False)


def map_data(request, quadrant="all", community="all", p_type="all", active=1):
    """ JSON API for Leaflet data """

    community = community.replace("_", " ")

    if active == 1:

        df = pd.DataFrame (
            list(
                RentalData.objects.using("rental_data").values(
                    "latitude", "longitude", "quadrant", "community", "price", "_type", "address", "sq_feet"
                )
                .filter(position="active")
            )
        )

    else:

        df = pd.DataFrame (
            list(
                RentalData.objects.using("rental_data").values(
                    "latitude", "longitude", "quadrant", "community", "price", "_type", "address", "sq_feet"
                )
            )
        )

    # Format quadrant names
    df = vf.quadrant_format(df)

    # Slice
    df = vf.query_slice(df, p_type, quadrant, community)

    # We only need price/sq feet
    df.drop(columns=["_type", "quadrant","community"], inplace=True)

    # Remove properties that have 0 dollars rent
    df = df.loc[(df.price > 100) & (df.price <10000)]

    # Remove properties that have 0 dollars rent
    df = df.loc[(df.sq_feet > 100) & (df.sq_feet <10000)]

    df.sq_feet = df.sq_feet.astype(int)

    df.dropna(inplace = True)

    flat = df.to_dict('records')

    return JsonResponse(flat, safe=False)
