from typing import List, Tuple

from sklearn.metrics import (  # type: ignore
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)


class MultiClassMetrics:
    def __init__(self) -> None:
        self.true_labels: List[str] = []
        self.predicted_labels: List[str] = []

    def update(self, true_label: str, predicted_label: str) -> None:
        # Update the lists of labels
        self.true_labels.append(true_label)
        self.predicted_labels.append(predicted_label)

    def get_precision_recall_f1(self, label: str) -> Tuple[float, float, float]:
        # Compute precision, recall, and F1 score for the given label
        precision = precision_score(
            self.true_labels, self.predicted_labels, labels=[label], average="macro"
        )
        recall = recall_score(
            self.true_labels, self.predicted_labels, labels=[label], average="macro"
        )
        f1 = f1_score(
            self.true_labels, self.predicted_labels, labels=[label], average="macro"
        )
        return precision, recall, f1

    def get_accuracy(self) -> float:
        # Compute accuracy
        return float(accuracy_score(self.true_labels, self.predicted_labels))

    def compute_weighted_average_metrics(self) -> dict:
        labels = list(
            set(self.true_labels + self.predicted_labels)
        )  # Get unique labels

        # Calculate weighted average precision, recall, F1 score, and accuracy
        weighted_precision = precision_score(
            self.true_labels, self.predicted_labels, labels=labels, average="weighted"
        )
        weighted_recall = recall_score(
            self.true_labels, self.predicted_labels, labels=labels, average="weighted"
        )
        weighted_f1 = f1_score(
            self.true_labels, self.predicted_labels, labels=labels, average="weighted"
        )
        accuracy = accuracy_score(self.true_labels, self.predicted_labels)

        # Calculate scores for each label
        label_scores = {}
        for label in labels:
            label_precision, label_recall, label_f1 = self.get_precision_recall_f1(
                label
            )
            label_scores[label] = {
                "Precision": label_precision,
                "Recall": label_recall,
                "F1": label_f1,
            }

        return {
            "Weighted Average": {
                "Precision": weighted_precision,
                "Recall": weighted_recall,
                "F1": weighted_f1,
                "Accuracy": accuracy,
            },
            "Scores by Label": label_scores,
        }

    def display_confusion_matrix(self) -> None:
        # Display the confusion matrix using sklearn's confusion_matrix function
        labels_list = sorted(set(self.true_labels + self.predicted_labels))
        cm = confusion_matrix(
            self.true_labels, self.predicted_labels, labels=labels_list
        )

        # Calculate the maximum label length for formatting purposes
        max_label_length = max([len(label) for label in labels_list])

        # Calculate the maximum width for the numbers based on the largest number in the confusion matrix
        max_number_width = max([len(str(num)) for row in cm for num in row])

        # Print header
        header = (
            " " * max_label_length
            + "\t"
            + "\t".join([label.rjust(max_number_width) for label in labels_list])
        )
        print(header)
        print("-" * len(header))  # Print a separator line

        # Print each row
        for i, label in enumerate(labels_list):
            row = (
                label.ljust(max_label_length)
                + "\t"
                + "\t".join(
                    [
                        str(cm[i, j]).rjust(max_number_width)
                        for j in range(len(labels_list))
                    ]
                )
            )
            print(row)
