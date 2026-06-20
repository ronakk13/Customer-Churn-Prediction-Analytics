CREATE DATABASE Customer_Churn;
USE Customer_Churn;


-- ===================================================
-- Customer analysis
-- ===================================================

SELECT
    Gender,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(
        SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0
        / COUNT(*),
        2
    ) AS churn_rate
FROM customer_churn
GROUP BY Gender;

SELECT 
      (CASE WHEN SeniorCitizen=1 THEN "Yes" ELSE "No" END) AS SeniorCitizen,
      COUNT(seniorcitizen) AS total_customer,
      SUM(CASE WHEN Churn="Yes" THEN 1 ELSE 0 END) AS churn,
      ROUND(
			SUM(CASE WHEN Churn="Yes" THEN 1 ELSE 0 END)*100.0
            /COUNT(*),
            2
		) AS churn_rate
	FROM customer_churn
	group by SeniorCitizen;
    
-- INSIGHTS
-- Senior Citizens show a churn rate of 41.7%, compared to 23.7%
-- for non-senior customers, making them one of the highest-risk customer groups.

SELECT 
	(CASE 
		WHEN tenure <= 15 THEN "New Customer"
		WHEN tenure <=40 THEN "Active Customer"
        ELSE "Loyal Customer"
	END) AS tenure_category,
    COUNT(*) AS total_customer,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(
        SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0
        / COUNT(*),
        2
    ) AS churn_rate
FROM customer_churn
GROUP BY tenure_category;

-- INSIGHTS
-- Focus retention efforts on customers during their first 15 months, where churn risk is highest.

-- ===================================================
-- Service Analysis
-- ===================================================

-- Churn by internet service
SELECT 
	InternetService,
    COUNT(*) AS Total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(
        SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0
        / COUNT(*),
        2
    ) AS churn_rate
FROM customer_churn	
GROUP BY InternetService;
    
-- INSIGHTS
-- Fiber Optic customers exhibit the highest churn rate (41.9%), more than double that of DSL customers


-- Churn by contract type
SELECT 
	Contract AS Contract_type,
    AVG(tenure) AS AVG_tenure_month,
    COUNT(*) AS Total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(
        SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0
        / COUNT(*),
        2
    ) AS churn_rate
FROM customer_churn
GROUP BY Contract_type;

-- INSIGHTS
-- Customers on Month-to-Month contracts are nearly 15x more likely to churn than customers on Two-Year contracts.

    
-- Churn by payment method
SELECT 
	PaymentMethod,
    COUNT(*) AS Total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(
        SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0
        / COUNT(*),
        2
    ) AS churn_rate
FROM customer_churn
GROUP BY PaymentMethod;

-- INSIGHTS
-- Electronic Check users represent the highest-risk payment segment with a churn rate exceeding 45%.




-- ===================================================
-- Revenue Analysis
-- ===================================================

SELECT 
	Contract,
    ROUND(SUM(TotalCharges),2) AS total_revenue,
    ROUND(SUM(CASE WHEN Churn="Yes" THEN TotalCharges ELSE 0 END),2) AS Revenue_loss,
    ROUND(
		SUM(CASE WHEN Churn="Yes" THEN TotalCharges ELSE 0 END)*100.0
		/SUM(TotalCharges),
	2) AS revenue_loss_pct,
    ROUND(
        SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0
        / COUNT(*),
        2
    ) AS churn_rate
FROM customer_churn
GROUP BY contract;

-- INSIGHTS
-- Month-to-Month customers contribute the majority of churn-related revenue loss.
	

-- ===================================================
--           High Risk Customer Profile
-- • New Customer
-- • Month-to-Month Contract
-- • Fiber Optic Service
-- • Electronic Check Payment
-- ===================================================

