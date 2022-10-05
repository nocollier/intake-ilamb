# ILAMB intake catalog

This code provides an `yaml`-style [intake](https://github.com/intake/intake) catalog of the reference data we use for ESM model benchmarking in the International Land Model Benchmarking ([ILAMB](https://www.ilamb.org)) effort.

Questions
---------
* How would we want to have users install this package? We could provide instructions for users to simply open a catalog which points to the remote `yaml` file. The following is a bit cumbersome, but works. Perhaps we can find a way to shrink the url. No matter what, users would have to come to documentation to remember a weird url. We could also put a `ilamb.yaml` somewhere easier to remember, like `https://www.ilamb.org/ilamb.yaml`.
```python
import intake
cat = intake.open_catalog("https://raw.githubusercontent.com/nocollier/intake-ilamb/main/ilamb.yaml")
```
* Alternatively, a user can clone this repository and then point `intake.open_catalog()` to the local `yaml` file. This feels way too complicated.
* In another sense, a user may want to install the data. That is, use the catalog to download all the data as described [here](https://intake.readthedocs.io/en/latest/data-packages.html#pure-conda-solution). We could use this as a vehicle to distribute and replace `ilamb-fetch`.
* We could make `intake_ilamb` which extends the API of `intake` like `intake-esm` does. For example, the following is from their examples. They have a url encoded in their source code, but they also add `open_esm_datastore()` to the `intake` API. 

```python
import intake
import intake_esm
cat_url = intake_esm.tutorial.get_url("google_cmip6")
cat = intake.open_esm_datastore(cat_url)
```
* We could have something similar. We could implement a simple extension of a `yaml` catalog which adds a catalog type to `intake` and also provides a `search()` function to help users find datasets.
```python
import intake
import intake_ilamb
cat_url = intake_ilamb.get_url("ILAMB") # could be "IOMB" or other collections
cat = intake.open_ilamb_cat(cat_url)
gpp = cat.search("gpp") # ['FLUXCOM|gpp','FLUXNET2015|gpp','WECANN|gpp']