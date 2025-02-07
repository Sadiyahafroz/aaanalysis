"""
This is a script for testing aa.comp_auc_adjusted function
"""
import numpy as np
import pytest
import hypothesis.strategies as some
from hypothesis import given, settings
import hypothesis.extra.numpy as npst
import aaanalysis as aa

# Set default deadline from 200 to 400
settings.register_profile("ci", deadline=400)
settings.load_profile("ci")


def check_invalid_conditions(X, labels, min_samples=3, check_unique=True):
    n_samples, n_features = X.shape
    n_unique_samples = len(set(map(tuple, X)))
    conditions = [
        (np.any(np.isinf(X)) or np.any(np.isnan(X)), "X contains NaN or Inf"),
        (n_samples < min_samples, f"n_samples={n_samples} should be >= {min_samples}"),
        (n_features < 2, f"n_features={n_features} should be >= 2"),
        (len(labels) != n_samples, "Length of labels should match n_samples."),
    ]
    if check_unique:
        conditions.append((n_unique_samples == 1, "Feature matrix 'X' should not have all identical samples."))
    for condition, msg in conditions:
        if condition:
            return True
    return False


def create_labels(size):
    labels = np.array([1, 2] + list(np.random.choice([1, 2], size=size-2)))
    return labels


class TestCompAucAdjusted:

    # Positive tests
    @settings(deadline=350, max_examples=20)
    @given(X=npst.arrays(dtype=np.float64, shape=npst.array_shapes(min_dims=2, max_dims=2),
                         elements=some.floats(min_value=-1e3, max_value=1e3, allow_nan=False, allow_infinity=False)))
    def test_X_positive(self, X):
        """Test with valid X input"""
        X = np.asarray(X)
        size = X.shape[0]
        if size >= 2:
            labels = create_labels(X.shape[0])
            is_invalid = check_invalid_conditions(X=X, labels=labels)
            if not is_invalid:
                label_test, label_ref = list(set(labels))
                assert isinstance(aa.comp_auc_adjusted(X, labels,
                                                       label_test=label_test,
                                                       label_ref=label_ref, n_jobs=1), np.ndarray)

    @settings(deadline=350, max_examples=20)
    @given(labels=some.lists(some.integers(min_value=1, max_value=2), min_size=2))
    def test_labels_positive(self, labels):
        """Test with valid labels input"""
        X = np.random.rand(len(labels), 3)
        size = X.shape[0]
        is_invalid = check_invalid_conditions(X=X, labels=labels)
        if not is_invalid and len(set(labels)) > 1 and size >= 2:
            label_test, label_ref = list(set(labels))
            assert isinstance(aa.comp_auc_adjusted(X, labels, label_test=label_test,
                                                   label_ref=label_ref, n_jobs=1), np.ndarray)

    def test_valid_n_jobs(self):
        """Test valid n_jobs input"""
        labels = create_labels(5)
        X = np.random.rand(len(labels), 3)
        label_test, label_ref = list(set(labels))
        assert isinstance(aa.comp_auc_adjusted(X, labels,
                                               label_test=label_test,
                                               label_ref=label_ref, n_jobs=4), np.ndarray)

    # Negative tests
    @settings(deadline=350, max_examples=20)
    @given(labels=some.lists(some.integers(min_value=1, max_value=2), min_size=2))
    def test_labels_negative(self, labels):
        """Test with invalid labels input (more than two unique values)."""
        X = np.random.rand(len(labels), 3)
        is_invalid = check_invalid_conditions(X=X, labels=labels)
        if is_invalid:
            with pytest.raises(ValueError):
                aa.comp_auc_adjusted(X, labels, label_ref=2, n_jobs=1)

    @settings(deadline=350, max_examples=20)
    @given(X=npst.arrays(dtype=np.float64, shape=npst.array_shapes(min_dims=2, max_dims=2),
                         elements=some.floats(min_value=-1e3, max_value=1e3, allow_nan=False, allow_infinity=False)))
    def test_X_negative(self, X):
        """Test with invalid X input (too few samples)."""
        X = np.asarray(X)
        labels = np.array([1] * len(X))
        is_invalid = check_invalid_conditions(X=X, labels=labels)
        if is_invalid:
            with pytest.raises(ValueError):
                aa.comp_auc_adjusted(X, labels, label_ref=2, n_jobs=1)

    def test_invalid_n_jobs(self):
        """Test invalid n_jobs input"""
        labels = create_labels(5)
        X = np.random.rand(len(labels), 3)
        label_test, label_ref = list(set(labels))
        with pytest.raises(ValueError):
            aa.comp_auc_adjusted(X, labels, label_test=label_test,
                                 label_ref=label_ref, n_jobs=0)
        with pytest.raises(ValueError):
            aa.comp_auc_adjusted(X, labels, label_test=label_test,
                                 label_ref=label_ref, n_jobs="Wrong")


class TestCompAucAdjustedComplex:

    @settings(deadline=350, max_examples=20)
    @given(X=npst.arrays(dtype=np.float64, shape=npst.array_shapes(min_dims=2, max_dims=2, min_side=1, max_side=10),
                         elements=some.floats(min_value=-1e3, max_value=1e3, allow_nan=False, allow_infinity=False)))
    def test_valid_input_combinations(self, X):
        """Test with valid combinations of X and labels."""
        X = np.asarray(X)
        size = X.shape[0]
        if size > 2:
            labels = create_labels(size)
            is_invalid = check_invalid_conditions(X=X, labels=labels)
            if len(X) == len(labels) and not is_invalid:
                label_test, label_ref = list(set(labels))
                assert isinstance(aa.comp_auc_adjusted(X, labels, label_test=label_test,
                                                       label_ref=label_ref, n_jobs=1), np.ndarray)

    @settings(deadline=350, max_examples=20)
    @given(X=npst.arrays(dtype=np.float64, shape=npst.array_shapes(min_dims=2, max_dims=2, min_side=1, max_side=10),
                         elements=some.floats(min_value=-1e3, max_value=1e3, allow_nan=False, allow_infinity=False)),
           labels=some.lists(some.integers(min_value=1, max_value=2), min_size=1, max_size=10))
    def test_invalid_input_combinations(self, X, labels):
        """Test with invalid combinations of X and labels (mismatched sizes)."""
        X = np.asarray(X)
        is_invalid = check_invalid_conditions(X=X, labels=labels)
        if is_invalid and len(X) != len(labels):
            with pytest.raises(ValueError):
                aa.comp_auc_adjusted(X, labels, n_jobs=1)
