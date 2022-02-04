# Constructing an industrial taxonomy using business website descriptions

!!! warning ":construction: Example under construction :construction:"

This example project is (loosely) based on work ongoing in `nestauk/industrial-taxonomy`, and the structure below is based on lessons learned in this project.

The project is split into four high-level tasks (:zero:, :one:, :two:, :three:) which we walk through.

Elements of :three: in particular have been simplified to keep the emphasis on the project structure rather than the project itself.

You can skip ahead to the [project tree :evergreen_tree:](./#project-tree) if you want a birds-eye view.

## :zero: Matching of Glass to Companies House

!!! abstract "Method"

    By fuzzy-matching data about UK business websites to Companies House based on company names we obtain a link between the text on business websites (describing businesses' activities) and the SIC codes (official industry codes) of that company.

    This work was performed in a separate project with the results stored and versioned in S3 by Metaflow. This can easily be retrieved using the metaflow client API.

:inbox_tray: `getters/inputs/{glass,companies_house.py,glass_house.py}`

: Fetch all the data via. metaflow's client API.

:mag_right: `analysis/eda`

: Exploratory data analysis of these data-sources

## :one: SIC classifier

!!! abstract "Method"

    Using the matched "glass-house" dataset train a classifier to predict SIC codes (this is developed as a general industry classifier that is agnostic to the SIC taxonomy as it is used elsewhere in the project).

    We can then conduct a meta-analysis looking at SIC codes that are under-represented by the classifiers predictions on validation data when compared to their "true" label obtained from the "glass-house" matching.

:material-pipe: `pipeline/industry_classifier/{log_reg_model.py,transformer_model.py}`

: Two competing models (not specific to SIC taxonomy)

:gear: `config/pipeline/industry_classifier/sic/*.yaml`

: Parameterisation of model flows.

    ??? question "What is the extra `sic` folder doing in the filepath?"

        There's an extra folder, `sic`, in the `config/` path that isn't present in the `pipeline/` path because this project uses the industry classifier models across different taxonomies.

        In this case, `sic` denotes the fact that we are applying it to the SIC taxonomy and gives us a namespace within the `config/` directory to isolate multiple uses of the same flow.


    ??? question "Whats with all the `config/pipeline/**/*.yaml`?"

        In this example structure, we have individual YAML files for each pipeline component.

        Whilst you are free to mimic this structure now, it is currently more convenient to nest the `config/pipeline/**` structure within `base.yaml` as it is easily importable as a python `dict` - `from src import config`.

        Furthermore, because metaflows are run from the command line and we want to parameterise them with YAML from `config/pipeline**`, each `flow.py` file currently needs an accompanying `run.py` file to:
        - Load and parse the YAML config needed for the pipeline
        - Form the pipeline arguments into a command to run the metaflow on the command line
        - Run the metaflow from within `run.py` using Python's `subprocess` library.
        - Update a config file with the successful metaflow run ID (so that getters know which version of the data to fetch)

        This is a lot of leg-work and increases the surface-area for bugs, you may be better off hard-coding values into shell-scripts or a Makefile.

:inbox_tray: `getters/outputs/sic_classifier.py`

: Load trained model, giving access to predict functionality

    ??? question "Why separate inputs and outputs in `getters/`?"

        Separating inputs and outputs in `getters` is useful when reading the code - it allows us to differentiate between what is produced in this project and what we depend on from elsewhere.

        This is less useful when writing code - the import `from src.getters.inputs.glass import get_sector` is very long. To provide a shorter import we can do the following:

        ```python
        # File: src/getters/__init__.py
        from .inputs import glass

        # File: src/analysis/example.py
        from src.getters.glass import get_sector
        ```

        Your directory structure doesn't always have to reflect the user-API!

    ??? failure "Avoid `import`ing from `src/pipeline/`"

        If you find yourself importing functions from `src/pipeline` in `src/analysis` then that functionality likely belongs in `src/utils`.

        Furthermore, `src/analysis` should get results of `src/pipeline` via. functions in `src/getters`.

        One exception that may occasionally arise when working with metaflow is needing to import a flow object itself - e.g. to access a static method or class method it defines (metaflow doesn't permit storing functions as data artifacts).

<!-- When using metaflow you should rarely need to `import` things from `pipeline/`.
Your getters can use the metaflow client API.

```python
def get_tokens():
    """Super informative documentation."""
    run_id = ... # Load from `config/`
    return metaflow.Run("MyFlow/{run_id}").data.tokens
```
-->

:mag_right: `analysis/sic_classifier/`

: Analysis of industry classifier models applied to SIC taxonomy

    - `model_selection.py` - Evaluate competing models and pick best
    - `sic_meta_analysis.py` - Meta-analysis looking at SIC codes under-represented in predictions and for which the model is over/under confident (informs which parts of the SIC taxonomy could be improved)

## :two: Hierarchical topic modelling

!!! abstract "Method"

    By training a [TopSBM hierarchical topic model](https://topsbm.github.io/) on the business website descriptions we can use the topics and clusters generated by the model and combine them with the SIC code labels to generate measures of sector similarity (how similar are any two SIC codes based on their cluster membership probabilities) and sector homogeneity (how homogeneous are is the topic distribution of descriptions aggregated by SIC code).

### Pre-processing

The first step is to process raw business website descriptions into clean, tokenised, n-grammed representation that can be passed to the topic model (this is re-used in :three:).

:material-pipe: `pipeline/glass_description_ngrams/{flow,utils}.py`

: Metaflow to run spacy entity recognition; convert to tokens; and generate n-grams based on co-occurrence

    !!! info "`flow.py` and `utils.py`"

        We have lots of `flow.py` and `utils.py`. Some might see this as bad because it's not super-informative; however as long as the parent folder has an informative name then it's good enough.

:gear: `config/glass_description_ngrams.yaml`

: Parameterisation of the above metaflow.

:inbox_tray: `getters/outputs/glass_house.py`

: Getter to fetch tokenised n-grams of business website descriptions.

:notebook_with_decorative_cover: `pipeline/glass_description_ngrams/notebooks/`

: Sanity-checking of output results. Not a part of `analysis/` because not directly analysing/presenting these results.

### Modelling

Now the topic model itself can be run.

:gear: `config/pipeline/topsbm.yaml`

: No corresponding flow in pipeline! Imported from a different library (e.g. `ds-utils`) and used here

:inbox_tray: `getters/outputs/topsbm.py`

: Fetch fitted model instance containing our inferred topics and clusters

:mag_right: `analysis/topsbm/`

: - `model_metadata.py` - Output summary table of model fit, other metadata such as topic hierarchy, top words etc. - `sector_similarity.py` - Pair-wise similarity of SIC codes calculated using topsbm model outputs - `sector_homogeneity.py` - Homogeneity of SIC codes calculated using topsbm model outputs - `utils.py` -

    ??? question "Hang on... Why is `section_*.py` not a pipeline component?"
        It would be equally valid to place these in `pipeline/` (because they are computing transformations of data) but `analysis/` is also fine (and possibly better) because:

        - Nothing else depends on these (so we aren't forced to refactor outside `analysis/`)</li>
        - The transformations done by these scripts are relatively quick (therefore there's no need to refactor into a metaflow in `pipeline/` to save others from having to recompute a long-running analysis)</li>
        - These scripts would need to exist anyway to visualise and summarise the results for reporting

    ??? question "Hang on... doesn't `utils.py` imply shared functionality in `analysis`?"

        If we had a flatter `analysis/` folder - e.g. everything in `analysis/topsbm/` was moved into `analysis/` - this would be unacceptable; however it's just about okay to have a short utils file here.

        If we weren't happy with this we could put it in `utils/topsbm.py`:
        - **For**: other pieces of analysis or pipeline components may need to use these functions in the future, now they can without refactoring
        - **Against**: in this case it's only one common function which we're pretty sure is only needed here and now lives further away from where it's used

## :three: Build a data-driven taxonomy

!!! abstract "Method"

    - Identify relevant terms within business website descriptions
    - Build a co-occurrence network of terms and prune network
    - Decompose co-occurrence into communities
    - Label companies with their communities to add a new level onto the existing SIC taxonomy
    - Apply industry classifier to perform similar meta-analysis to that done in :one:

### Keyword extraction

Use keyword extraction methods to tag business descriptions with items from the UNSPSC (a products and services taxonomy).
Given this is successful, co-occurrence networks of products and services can be used to build a taxonomy. If this is unsuccessful, fall back on the n-gramming pipeline produced in :two:.

:floppy_disk: `inputs/data/UNSPSC_English_v230701.xlsx`

: New dataset for this project provided by the supplier as an excel spreadsheet

:mag_right: `analysis/eda/unspsc.py`

: Explore the UNSPSC dataset

:inbox_tray: `getters/inputs/unspsc.py`

: Function to load UNSPSC data

    - Note: It's structured and clean enough that we don't need to do any preprocessing on it

:material-pipe: `pipeline/keyword_extraction/*.py`

: Metaflows to extract keywords from text using various methods and filter based on prescence in UNSPSC

:gear: `config/pipeline/keyword_extraction/*.yaml`

: Parameterise above pipelines

:notebook_with_decorative_cover: `analysis/keyword_extraction/notebooks/`

: !!! info "None of the keyword extraction approaches worked out"
No need to refactor notebooks into script if materials are not produced for final reporting.

    Notebooks exploring results of keyword extraction methods and comparing their effectiveness.

### N-gramming pipeline

:gear: `getters/outputs/glass_house.py`

: Use same getter as produced in [preprocessing step of :two:](./#pre-processing).

### Constructing a term co-occurrence network and generating communities

:material-pipe: `pipeline/kw_cooccurrence_taxonomy/*.py`

: Metaflow and utils to construct a co-occurrence network of terms; decompose into communities; and label companies with their community labels

:gear: `config/pipeline/kw_cooccurrence_taxonomy.yaml`

: Parameterise above flow

:mag_right: `analysis/kw_cooccurrence_taxonomy/visualise_structure.py`

: Visualise the structure of the new taxonomy (and it's dependent communities)

### Applying the industry classifier to the new taxonomy level

:gear: `config/pipeline/industry_classifier/kw_cooccurrence_taxonomy.yaml`

: Apply the industry classifier to our new taxonomies labels

:mag_right: `analysis/kw_cooccurrence_taxonomy/industry_classifier.py`

: Perform a meta-analysis for our new taxonomy as was done in :one: for the SIC taxonomy

## :evergreen_tree: Project tree

=== "folders only"

    ```shell
    ├── inputs
    │   └── data
    └── src
        ├── analysis
        │   ├── eda
        │   │   └── notebooks
        │   ├── keyword_extraction
        │   ├── kw_cooccurrence_taxonomy
        │   │   └── notebooks
        │   ├── sic_classifier
        │   │   └── notebooks
        │   └── topsbm
        ├── config
        │   └── pipeline
        │       └── industry_classifier
        │           ├── kw_cooccurrence_taxonomy
        │           └── sic
        ├── getters
        │   ├── inputs
        │   └── outputs
        ├── pipeline
        │   ├── glass_description_ngrams
        │   ├── industry_classifier
        │   │   └── notebooks
        │   ├── keyword_extraction
        │   │   └── notebooks
        │   ├── kw_cooccurrence_taxonomy
        │   │   └── notebooks
        │   └── sic_taxonomy_data
        └── utils
            ├── altair
            └── metaflow
    ```

=== "folders and files"

```
TODO
```

<!--
    ```nohighlight
    ├── inputs
    │   └── data
    │       └── UNSPC_English_v230701.xlsx
    └── src
        ├── analysis
        │   ├── eda
        │   │   ├── glass_house.py
        │   │   ├── glass.py
        │   │   └── notebooks
        │   ├── keyword_extraction
        │   │   └── comparison.py
        │   ├── kw_cooccurrence_taxonomy
        │   │   ├── apply_sic_classifier.py
        │   │   ├── comparison_to_sic.py
        │   │   ├── notebooks
        │   │   └── visualise_structure.py
        │   ├── sic_classifier
        │   │   ├── model_selection.py
        │   │   ├── notebooks
        │   │   └── sic_meta_analysis.py
        │   └── topsbm
        │       ├── model_metadata.py
        │       ├── sector_homogeneity.py
        │       ├── sector_similarity.py
        │       └── utils.py
        ├── config
        │   ├── base.yaml
        │   ├── logging.yaml
        │   └── pipeline
        │       ├── glass_description_ngrams.yaml
        │       ├── industry_classifier
        │       │   ├── kw_cooccurrence_taxonomy
        │       │   │   └── transformer.yaml
        │       │   └── sic
        │       │       ├── log_reg_model.yaml
        │       │       └── transformer_model.yaml
        │       ├── kw_cooccurrence_taxonomy.yaml
        │       ├── sic_taxonomy_data.yaml
        │       └── topsbm.yaml
        ├── getters
        │   ├── __init__.py
        │   ├── inputs
        │   │   ├── companies_house.py
        │   │   ├── glass_house.py
        │   │   ├── glass.py
        │   │   └── unspsc.py
        │   └── outputs
        │       ├── glass_house.py
        │       ├── industry_classifier.py
        │       ├── sic_taxonomy.py
        │       ├── topsbm.py
        │       └── unspsc_keywords.py
        ├── __init__.py
        ├── pipeline
        │   ├── glass_description_ngrams
        │   │   ├── flow.py
        │   │   └── utils.py
        │   ├── industry_classifier
        │   │   ├── log_reg_model.py
        │   │   ├── notebooks
        │   │   │   └── prototype_model.ipynb
        │   │   ├── transformer_model.py
        │   │   └── utils.py
        │   ├── __init__.py
        │   ├── keyword_extraction
        │   │   ├── fit_keybert.py
        │   │   ├── fit_rake.py
        │   │   ├── fit_yake.py
        │   │   ├── notebooks
        │   │   └── utils.py
        │   ├── kw_cooccurrence_taxonomy
        │   │   ├── flow.py
        │   │   ├── notebooks
        │   │   └── utils.py
        │   └── sic_taxonomy_data
        │       ├── flow.py
        │       └── utils.py
        └── utils
            ├── altair
            │   ├── export.py
            │   └── minimap_bar_chart.py
            ├── cache.py
            ├── __init__.py
            └── metaflow
                ├── bundle.py
                ├── client.py
                ├── config.py
                ├── decorators.py
                └── runner.py
    ``` -->
