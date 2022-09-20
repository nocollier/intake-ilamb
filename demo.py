"""Simple demonstration of how ILAMB catalogs could work (in progress)"""
from typing import Iterable

import intake

# Load the ILAMB catalog and list its contents. One item is a pointer to another
# catalog that I have called 'ilamb-raw' and contains sources which point back
# to data that that ILAMB collection is built from.
#
cat = intake.open_catalog("ilamb.yaml")
print(list(cat))

# Catalogs can be nested. You can de-reference them using the string hash and
# print the contents the same as before. This reveals a few raw datasets that I
# have been working on encoding. Not all of them work and I am trying to figure
# out caching in some.
nest_cat = cat["ilamb-raw"]
print(list(nest_cat))

# For example, if you install `intake-thredds` then you can load the CLASS data
# catalog, which points to a remote THREDDS catalog.
src = nest_cat["CLASS"]
print(src)

# The `src` variable here just describes the data source--no data has yet been
# trasferred. But when we issue the read() function, then data is downloaded and
# merged automatically. If you look at the arguments in the `src` you will see
# that I have specified concatenation of the catalog files in the `time`
# dimension. The only issue here is that I have not yet figured out the
# filecaching. When I specify a caching scheme, it seems to cache the catalog
# file, not the merged dataset.
#
# 'data' is then a merged xarray dataset with all the years available. The nice
# thing about this is if they added years on their end, I would pick it up
# automatically.
data = src.read()

# I envision having a catalog of the raw data ILAMB uses as well as our
# processed versions--both could have their uses. Note that for now the data
# hosted on ilamb.org will not download. I do not understand all the issues, but
# essentially many OSs believe our certificate authority is out of date (which
# it isn't). Forrest has a fix in mind but no time to execute it just yet.
#
# I like intake, but there are a few things that as of yet aren't as nice as my
# ilamb-fetch:
#  1) while data can be cached locally, it is somewhat invisible to you how and
#     where
#  2) the data may be cached, but there are no checks (as far as I know) for
#     check that your cache is up to date with the remote version
#  3) you depend on someone having written a compatible plugin or that the
#     provider gives you access. For example, the MPI data portal has a custom
#     system where you give it an email and they send you a temporary link where
#     you can download the data.

# But you can envision building a ILAMB catalog with a nice search capability.
# Depending on how you choose to populate metadata, you can write search
# functions so users can see what is available.
def search_for_variable(cat: intake.Catalog, variable: str, found: list = []):
    """search the catalog for a given variable"""
    for i in cat:
        if isinstance(cat[i], Iterable):
            search_for_variable(cat[i], variable, found)
        else:
            if (
                "variables" in cat[i].metadata
                and variable in cat[i].metadata["variables"]
            ):
                found.append(cat[i])
    return found


fnd = search_for_variable(cat, "gpp")
for f in fnd:
    print(f)
