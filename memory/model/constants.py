class FeatureColumns:
    POOL = "pool"
    USE_MEM = "useMemMB"
    FEATURES = ['mLayer', 'mSize', 'mFiles', 'events', 'agg', 'exg', 'alt',
                'select', 'hjoin', 'ljoin', 'scan', 'sort', 'union', 'top']

LABEL = "label"
PREDICT_MEM = "predictMemMB"
FEATURE_NUM = 12
COLUMNS_CLEAN_FUNC = {'mSize': round, 'mFiles': round, 'useMemMB': round}
MEMORY_SPLIT = [50, 200, 300, 500, 800, 1500, 5000]
ACCURACY_SPLIT = [500, 1000, 2000, 5000]
CLASS_NUM = 4
CROSS_VALIDATE_RATIO = 0.67
MEMORY_PREDICT_RATIO = 0.5
MODEL_GROUP = [
    {
        'name': "first",
        'pool_group': ["root.hadoop-ad", "root.hadoop-tvd", "root.hadoop-am",
                       'root.app-ad']
    },
    {
        'name': "second",
        'pool_group': ['root.app-gwd', 'root.hadoop-wd']
    },
    {
        'name': "third",
        'pool_group': ["root.consultant", "root.dm-pool"]
    },
    {
        'name': "fourth",
        'pool_group': ["root.datascience", "root.default"]
    },
    {
        'name': "fifth",
    }
]
