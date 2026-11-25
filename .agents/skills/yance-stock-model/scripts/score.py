"""Apply Yance V3.0 gates to final Q, B, P scores. Does not score evidence."""
import argparse
import json
from decimal import Decimal, InvalidOperation


def parse_score(value):
    try:
        score = Decimal(value)
    except InvalidOperation as error:
        raise argparse.ArgumentTypeError("请输入 0 到 100 的有限分数") from error
    if not score.is_finite() or not 0 <= score <= 100:
        raise argparse.ArgumentTypeError("请输入 0 到 100 的有限分数")
    return score


def evaluate(q, b, p):
    total = q * Decimal("0.45") + b * Decimal("0.25") + p * Decimal("0.30")
    if q >= 90 and b >= 85 and p >= 85 and total >= 88:
        tier = "S 级三高"
    elif q >= 85 and b >= 80 and p >= 80 and total >= 83:
        tier = "黄金三高"
    elif q >= 80 and b >= 70 and p >= 70:
        tier = "核心参与区"
    else:
        tier = "未进核心参与区"

    numeric_setups = []
    if q >= 80 and b >= 70 and p >= 80:
        numeric_setups.append("右侧突破")
    if q >= 80 and b >= 80 and p >= 70:
        numeric_setups.append("强势回踩")
    if q >= 85 and b >= 80 and p < 55:
        numeric_setups.append("左侧试错")
    return {
        "Q": str(q), "B": str(b), "P": str(p), "T": str(total),
        "最高资格": tier,
        "满足分数条件的模式，形态须另核": numeric_setups,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("Q", "B", "P"):
        parser.add_argument(name, type=parse_score)
    scores = parser.parse_args()
    print(json.dumps(evaluate(scores.Q, scores.B, scores.P), ensure_ascii=False))
