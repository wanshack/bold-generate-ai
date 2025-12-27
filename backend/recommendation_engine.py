from typing import Dict, Any
from database import get_supabase_client
from datetime import datetime

class RecommendationEngine:
    def __init__(self):
        self.supabase = get_supabase_client()

    def generate_recommendation(
        self,
        stock_id: str,
        current_price: float,
        predicted_price: float,
        prediction_confidence: float,
        technical_analysis: Dict,
        financial_data: Dict = None
    ) -> Dict[str, Any]:
        price_change_pct = ((predicted_price - current_price) / current_price) * 100
        technical_score = technical_analysis.get("score", 0.5)

        fundamental_score = self._calculate_fundamental_score(financial_data) if financial_data else 0.5

        combined_score = (technical_score * 0.4) + (fundamental_score * 0.3) + (prediction_confidence * 0.3)

        if price_change_pct > 10 and combined_score > 0.65:
            action = "buy"
            risk_level = "medium"
        elif price_change_pct < -10 and combined_score < 0.35:
            action = "sell"
            risk_level = "high"
        elif price_change_pct > 5 and combined_score > 0.6:
            action = "buy"
            risk_level = "low"
        elif price_change_pct < -5 and combined_score < 0.4:
            action = "sell"
            risk_level = "medium"
        else:
            action = "hold"
            risk_level = "low"

        if abs(price_change_pct) > 15:
            time_horizon = "short"
        elif abs(price_change_pct) > 8:
            time_horizon = "medium"
        else:
            time_horizon = "long"

        reasoning = self._generate_reasoning(
            action,
            price_change_pct,
            technical_score,
            fundamental_score,
            technical_analysis.get("signals", []),
            financial_data
        )

        target_price = predicted_price if action in ["buy", "hold"] else current_price * 0.95

        recommendation = {
            "stock_id": stock_id,
            "action": action,
            "confidence_score": combined_score,
            "target_price": target_price,
            "current_price": current_price,
            "technical_score": technical_score,
            "fundamental_score": fundamental_score,
            "reasoning": reasoning,
            "risk_level": risk_level,
            "time_horizon": time_horizon
        }

        return recommendation

    def _calculate_fundamental_score(self, financial_data: Dict) -> float:
        if not financial_data or "info" not in financial_data:
            return 0.5

        info = financial_data["info"]
        score = 0.5

        if info.get("trailingPE"):
            pe = info["trailingPE"]
            if pe < 15:
                score += 0.1
            elif pe > 30:
                score -= 0.1

        if info.get("priceToBook"):
            pb = info["priceToBook"]
            if pb < 1.5:
                score += 0.1
            elif pb > 3:
                score -= 0.05

        if info.get("returnOnEquity"):
            roe = info["returnOnEquity"]
            if roe > 0.15:
                score += 0.15
            elif roe < 0.05:
                score -= 0.1

        if info.get("debtToEquity"):
            de = info["debtToEquity"]
            if de < 0.5:
                score += 0.1
            elif de > 2:
                score -= 0.15

        if info.get("revenueGrowth"):
            growth = info["revenueGrowth"]
            if growth > 0.15:
                score += 0.1
            elif growth < 0:
                score -= 0.1

        return max(0.0, min(1.0, score))

    def _generate_reasoning(
        self,
        action: str,
        price_change_pct: float,
        technical_score: float,
        fundamental_score: float,
        technical_signals: list,
        financial_data: Dict
    ) -> str:
        reasoning_parts = []

        reasoning_parts.append(
            f"**Price Prediction:** Our ML model predicts a {abs(price_change_pct):.2f}% "
            f"{'increase' if price_change_pct > 0 else 'decrease'} in the stock price over the next 30 days."
        )

        reasoning_parts.append(
            f"\n**Technical Analysis (Score: {technical_score:.2f}/1.00):** "
        )
        if technical_signals:
            reasoning_parts.append("Key signals include: " + "; ".join(technical_signals[:3]) + ".")
        else:
            reasoning_parts.append("Technical indicators show neutral sentiment.")

        reasoning_parts.append(
            f"\n**Fundamental Analysis (Score: {fundamental_score:.2f}/1.00):** "
        )
        if financial_data and "info" in financial_data:
            info = financial_data["info"]
            fund_insights = []

            if info.get("trailingPE"):
                fund_insights.append(f"P/E ratio of {info['trailingPE']:.2f}")
            if info.get("returnOnEquity"):
                fund_insights.append(f"ROE of {info['returnOnEquity']*100:.2f}%")
            if info.get("debtToEquity"):
                fund_insights.append(f"Debt/Equity ratio of {info['debtToEquity']:.2f}")

            if fund_insights:
                reasoning_parts.append("Company fundamentals show " + ", ".join(fund_insights) + ".")
            else:
                reasoning_parts.append("Limited fundamental data available.")
        else:
            reasoning_parts.append("Fundamental data not available for analysis.")

        if action == "buy":
            reasoning_parts.append(
                f"\n**Recommendation:** BUY - Strong bullish signals with positive price momentum. "
                f"Both technical and fundamental indicators support upward movement."
            )
        elif action == "sell":
            reasoning_parts.append(
                f"\n**Recommendation:** SELL - Bearish indicators suggest downward pressure. "
                f"Consider reducing exposure or taking profits."
            )
        else:
            reasoning_parts.append(
                f"\n**Recommendation:** HOLD - Mixed signals suggest waiting for clearer direction. "
                f"Monitor for breakout patterns or fundamental changes."
            )

        reasoning_parts.append(
            "\n⚠️ **Disclaimer:** This recommendation is generated by AI and should not be considered "
            "financial advice. Always conduct your own research and consult with a licensed financial "
            "advisor before making investment decisions."
        )

        return "".join(reasoning_parts)

    def save_recommendation(self, recommendation: Dict) -> Dict:
        result = self.supabase.table("recommendations").insert(recommendation).execute()
        return result.data[0] if result.data else None
