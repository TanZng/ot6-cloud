# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:hydrogen
#     text_representation:
#       extension: .py
#       format_name: hydrogen
#       format_version: '1.3'
#       jupytext_version: 1.14.4
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
import pandas as pd
import vaex
import glob


# %%
# Load certain folders
folders = ["17_12_2022"]

files = []
for fold in folders:
    files += glob.glob(f'/home/jovyan/work/data/{fold}/*.parquet.zst')

    # Show first 5 folders
files[:5]

# %% [markdown]
# # Pandas

# %%
pdf = pd.concat([pd.read_parquet(fp) for fp in files])


# %%
type(pdf)

# %%
pdf.tail(5)

# %% [markdown]
# # Vaex

# %%
vdf = vaex.from_pandas(pdf)

# %%
type(vdf)

# %%
vdf.tail(5)

# %%
categories = vdf.productCategory.values # convert to list
print(categories)

# %%
