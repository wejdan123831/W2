## Key Analysis Findings (Audit Results)


##  question 1: how does purchasing power (Amount) differ between different countries
During the data audit and exploratory analysis (EDA), several critical patterns were identified using our standard comparison metrics (Mean vs Median):

### 1. Purchasing Power Skewness
* **Finding**: In the Saudi Arabia (SA) market, the **Mean (35.85)** is nearly double the **Median (18.75)**.
* **Interpretation**: This confirms that "Average hides skew." Most customers spend around 18.75, but a few high-value orders (outliers) are pulling the average up.
* **Business Impact**: Pricing strategies should target the median range to remain competitive for the majority of users.

### 2. High-Value Segment (P90)
* **Finding**: The **P90 value (75.93)** indicates that the top 10% of orders are significantly higher than the rest of the population.
* **Insight**: This highlights a clear "VIP" segment that could be targeted with premium loyalty programs.

### 3. Data Quality Issues (Audit)
* **Finding**: The **AE (UAE)** group shows zero samples ($n=0$) and missing values.
* **Recommendation**: Immediate investigation into the ETL pipeline is required to ensure UAE data is being captured and processed correctly.



##  question 3: How does the revenue trend evolve over time on a monthly basis?

Interpretations :

Revenue Growth: The monthly trend shows a total revenue of 45.64 for December 2025 across 4 orders.

Skewness Awareness: By comparing the Mean (15.21) and Median (12.5), we observe that the average is slightly higher than the median, indicating a minor positive skew even in monthly aggregates.

High-End Purchases: The P90 value (22.5) reveals that the top 10% of transactions are nearly double the median, suggesting a small but significant segment of higher-value order. 

Caveats :

Limited Timeframe: The dataset currently shows only one active month (2025-12), which is insufficient to determine long-term seasonality or growth trends.
Missing Data: The presence of an <NA> month in the table with 1 order suggests there are records with missing date information that need audit investigation.
Small Sample Size: With only $n=4$ for the main month, the statistical metrics (like Mean and P90) are highly sensitive to any single new order


##  question 3 What is the relationship between 'order status' and average transaction amounts? Does a higher transaction value increase the likelihood of failure or refund?

1. Interpretations
High-Value Success: The data shows that high-ticket orders are not prone to failure; the Mean (35.85) for paid orders is nearly double the Median (18.75), confirming that the largest amounts in the dataset were successfully completed.

Refund Isolation: There is no evidence of high-value refunds. The "Refund" status shows zero total revenue and missing values for mean and median, suggesting that significant financial volume is currently safe from reversals.

VIP Stability: The P90 (75.93) for successful orders indicates that our most valuable customers (top 10%) have a high success rate in completing their transactions without payment rejections.

2. Caveats
Data Logging Bias: The missing values (<NA>) for refund amounts suggest a potential audit issue where original values might be cleared during the refund process rather than the orders being small.

Extreme Skewness: Because the mean is significantly higher than the median, the business is highly dependent on a few large transactions. Any single failure of a high-value order in the future will drastically impact the overall average.

Sample Limitation: With a total count of only n=5 across all statuses, these findings are directional and require a larger dataset to be statistically conclusive

## Next questions
Why is the highest-value order (97.75) failing to record a created_at date?

Is the lack of UAE data a technical bug in the country matching logic?

If we expand the sample size, does the P90 value stabilize or continue to grow?