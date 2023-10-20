import pytest

from okareo.metrics import MultiClassMetrics


@pytest.fixture
def metrics() -> MultiClassMetrics:
    m = MultiClassMetrics()
    true_labels = ["cat", "dog", "bird", "cat", "bird"]
    predicted_labels = ["dog", "dog", "bird", "cat", "cat"]
    for true, predicted in zip(true_labels, predicted_labels):
        m.update(true, predicted)
    return m


def test_update(metrics: MultiClassMetrics) -> None:
    assert metrics.true_labels == ["cat", "dog", "bird", "cat", "bird"]
    assert metrics.predicted_labels == ["dog", "dog", "bird", "cat", "cat"]


def test_get_accuracy(metrics: MultiClassMetrics) -> None:
    accuracy = metrics.get_accuracy()
    assert accuracy == 0.6  # 3 correct out of 5


def test_compute_weighted_average_metrics(metrics: MultiClassMetrics) -> None:
    results = metrics.compute_weighted_average_metrics()
    assert "Weighted Average" in results
    assert "Scores by Label" in results
    # Further asserts can be added based on expected values


def test_get_precision_recall_f1_for_cat(metrics: MultiClassMetrics) -> None:
    precision, recall, f1 = metrics.get_precision_recall_f1("cat")
    assert precision == 0.5  # 1 TP, 1 FP
    assert recall == 0.5  # 1 TP, 1 FN
    assert f1 == 0.5  # Harmonic mean of precision and recall


def test_get_precision_recall_f1_for_dog(metrics: MultiClassMetrics) -> None:
    precision, recall, f1 = metrics.get_precision_recall_f1("dog")
    assert precision == 0.5  # 1 TP, 1 FP
    assert recall == 1.0  # 1 TP, 0 FN
    assert f1 == 2 / (1 / 0.5 + 1 / 1.0)  # Harmonic mean of precision and recall


def test_get_precision_recall_f1_for_bird(metrics: MultiClassMetrics) -> None:
    precision, recall, f1 = metrics.get_precision_recall_f1("bird")
    assert precision == 1.0  # 1 TP, 0 FP
    assert recall == 0.5  # 1 TP, 1 FN
    assert f1 == 2 / (1 / 1.0 + 1 / 0.5)  # Harmonic mean of precision and recall
