from .model.util import label_to_mem
from .error import ParameterError
from .model.constants import MODEL_GROUP
from .util import ModelFactory


def get_model(pool):
    """get model suits current specified pool.
    :param pool: pool name, specified by post params

    """
    for g in MODEL_GROUP:
        # if g['pool_group'] contains pool or
        # pool is "default" and g has no 'pool_group' key
        if (pool == 'default' and not g.get('pool_group')) or pool in \
                repr(g['pool_group']):
            return ModelFactory.get_model(g['name'])
    raise ParameterError(message="pool %s not found" % pool)


def predict(m, features):
    label = m.clf.predict([[features.get(f) for f in m.features]])
    mem = label_to_mem(label, m.class_predict)
    return mem
