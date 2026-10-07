"""sklearn-vs-C parity for emlearn_linear (fixed seeds, deterministic).

The GENERATED C is compiled with TDM-GCC (-Wall -Wextra -Werror) and run over
fixed test vectors; outputs must match sklearn. See gcc_harness.py for why
upstream CompiledClassifier (MSVC-bound on Windows) is not used here.
"""

import os

import numpy
import pytest

sklearn = pytest.importorskip('sklearn')
from sklearn.linear_model import LogisticRegression, LinearRegression  # noqa: E402

from emlearn_linear import Wrapper  # noqa: E402
from gcc_harness import compile_and_run  # noqa: E402

TMP = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tmp_parity')


def _binary_data():
    rng = numpy.random.RandomState(0)
    X = rng.uniform(-3, 3, size=(60, 2))
    y = (X[:, 0] + 0.5 * X[:, 1] > 0).astype(int)
    return X, y


def _multi_data():
    rng = numpy.random.RandomState(1)
    X = rng.uniform(-3, 3, size=(90, 3))
    y = numpy.argmax(numpy.stack([
        X[:, 0], X[:, 1] + 1.0, -X[:, 0] - X[:, 1],
    ]), axis=0)
    return X, y


def _reg_data():
    rng = numpy.random.RandomState(2)
    X = rng.uniform(-2, 2, size=(50, 2))
    y = 1.5 * X[:, 0] - 0.7 * X[:, 1] + 0.3
    return X, y


def test_binary_predict_parity(tmp_path):
    X, y = _binary_data()
    est = LogisticRegression().fit(X, y)
    code = Wrapper(est).save(name='lin')
    got = [int(v) for v in compile_and_run(code, 'lin', X, 'predict',
                                           workdir=str(tmp_path))]
    assert got == list(est.predict(X))


def test_binary_proba_parity(tmp_path):
    X, y = _binary_data()
    est = LogisticRegression().fit(X, y)
    code = Wrapper(est).save(name='lin')
    rows = compile_and_run(code, 'lin', X, 'proba', n_classes=2,
                           workdir=str(tmp_path))
    got = numpy.array([[float(v) for v in r.split(',')] for r in rows])
    want = est.predict_proba(X)
    assert got.shape == want.shape
    assert numpy.max(numpy.abs(got - want)) < 1e-5


def test_multiclass_predict_and_proba_parity(tmp_path):
    X, y = _multi_data()
    est = LogisticRegression(multi_class='multinomial', max_iter=2000).fit(X, y)
    code = Wrapper(est).save(name='lin')
    got = [int(v) for v in compile_and_run(code, 'lin', X, 'predict',
                                           workdir=str(tmp_path))]
    assert got == list(est.predict(X))
    rows = compile_and_run(code, 'lin', X, 'proba', n_classes=3,
                           workdir=str(tmp_path))
    gotp = numpy.array([[float(v) for v in r.split(',')] for r in rows])
    wantp = est.predict_proba(X)
    assert gotp.shape == wantp.shape
    assert numpy.max(numpy.abs(gotp - wantp)) < 1e-5


def test_nonstandard_labels_mapped(tmp_path):
    X, y = _binary_data()
    y = numpy.where(y == 1, 7, 5)
    est = LogisticRegression().fit(X, y)
    code = Wrapper(est).save(name='lin')
    got = [int(v) for v in compile_and_run(code, 'lin', X, 'predict',
                                           workdir=str(tmp_path))]
    assert got == list(est.predict(X))


def test_single_feature_binary(tmp_path):
    rng = numpy.random.RandomState(3)
    X = rng.uniform(-2, 2, size=(40, 1))
    y = (X[:, 0] > 0.5).astype(int)
    est = LogisticRegression().fit(X, y)
    code = Wrapper(est).save(name='lin')
    got = [int(v) for v in compile_and_run(code, 'lin', X, 'predict',
                                           workdir=str(tmp_path))]
    assert got == list(est.predict(X))


def test_regression_parity(tmp_path):
    X, y = _reg_data()
    est = LinearRegression().fit(X, y)
    code = Wrapper(est).save(name='lin')
    got = numpy.array([float(v) for v in compile_and_run(
        code, 'lin', X, 'regress', workdir=str(tmp_path))])
    want = est.predict(X)
    assert numpy.max(numpy.abs(got - want)) < 1e-4


def test_generated_c_has_no_python_deps():
    X, y = _binary_data()
    est = LogisticRegression().fit(X, y)
    code = Wrapper(est).save(name='comfort')
    assert '#include <stdint.h>' in code
    assert 'comfort_predict' in code
    for banned in ('numpy', 'sklearn', 'import ', 'PyObject'):
        assert banned not in code


def test_rejects_unfitted_and_unsupported():
    with pytest.raises(ValueError):
        Wrapper(LogisticRegression())
    with pytest.raises(ValueError):
        from sklearn.tree import DecisionTreeClassifier
        Wrapper(DecisionTreeClassifier())
