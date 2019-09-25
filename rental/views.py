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


def time_series(request, quadrant, p_type, active=1):

    if(active == 1):

        df = pd.DataFrame(
            list(
                RentalData.objects.using('rental_data')
                .values('_type', 'price', 'quadrant')
                .filter(position='active')
            )
        )

    else:

        df = pd.DataFrame(
            list(
                RentalData.objects.using('rental_data')
                .values('_type', 'price', 'quadrant')
            )
        )

    # Remove properties that have 0 dollars rent
    df = df[df.price != 0]

    df.set_index('retrieval_date', inplace=True)

    df = df.sort_index()

    df = vf.quadrant_format(df)

    df = df[(df['_type'] == p_type) & (df['quadrant'] == quadrant)].dropna()

    df.drop(columns=['_type', 'quadrant'], inplace=True)

    agg = df.groupby(df.index).mean()

    flat = agg.to_dict()

    return JsonResponse(flat, safe=False)


def price_metrics(request, fun, quadrant="all", p_type="all", active=1):

    if(active == 1):

        df = pd.DataFrame(
            list(
                RentalData.objects.using('rental_data')
                .values('_type', 'price', 'quadrant')
                .filter(position='active')
            )
        )

    else:

        df = pd.DataFrame(
            list(
                RentalData.objects.using('rental_data')
                .values('_type', 'price', 'quadrant')
            )
        )

    df = vf.quadrant_format(df)

    if(quadrant != "all"):
        df = df[(df['_type'] == p_type)]

    if(p_type != "all"):
        df = df[(df['quadrant'] == quadrant)]

    # Remove properties that have 0 dollars rent
    df = df[df.price != 0]

    if fun == 'avg':
        val = df['price'].mean()
    elif fun == 'min':
        val = df['price'].min()
    elif fun == 'max':
        val = df['price'].max()
    else:
        val = df['price'].mean()

    val = round(val)

    return JsonResponse({"fun": fun, "quadrant": quadrant, "p_type": p_type, "val": val}, safe=False)


def listing_count(request, quadrant="all", p_type="all", active=1):

    if(active == 1):

        df = pd.DataFrame(
            list(
                RentalData.objects.using('rental_data')
                .values('_type', 'price', 'quadrant')
                .filter(position='active')
            )
        )

    else:

        df = pd.DataFrame(
            list(
                RentalData.objects.using('rental_data')
                .values('_type', 'price', 'quadrant')
            )
        )

    # Remove properties that have 0 dollars rent
    df = df[df.price != 0]

    df = vf.quadrant_format(df)

    if(quadrant != "all"):
        df = df[(df['_type'] == p_type)]

    if(p_type != "all"):
        df = df[(df['quadrant'] == quadrant)]

    val = df.shape[0]

    return JsonResponse({"quadrant": quadrant, "p_type": p_type, "count": val}, safe=False)


def map_data(request):
    """ JSON API """

    data = list(
        RentalData.objects.using('rental_data')
        .values('latitude', 'longitude', 'price', '_type', 'address', 'sq_feet')
        .filter(position='active')
    )

    from django.core.serializers import serialize

    return JsonResponse(data, safe=False)