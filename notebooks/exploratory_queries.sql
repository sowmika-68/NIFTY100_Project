SELECT COUNT(*) AS total_companies
FROM companies;

SELECT
company_name,
roe_percentage
FROM companies
ORDER BY roe_percentage DESC
LIMIT 10;

SELECT
company_id,
MAX(sales) AS highest_sales
FROM profitandloss
GROUP BY company_id
ORDER BY highest_sales DESC
LIMIT 10;

SELECT
AVG(roe_percentage) AS avg_roe
FROM companies;

SELECT
company_name
FROM companies
WHERE website IS NULL
OR website='';

SELECT
company_id,
MAX(net_profit) AS max_profit
FROM profitandloss
GROUP BY company_id
ORDER BY max_profit DESC
LIMIT 10;

SELECT
company_id,
MAX(dividend_payout) AS dividend
FROM profitandloss
GROUP BY company_id
ORDER BY dividend DESC
LIMIT 10;

SELECT
sector,
COUNT(*) AS companies
FROM sectors
GROUP BY sector
ORDER BY companies DESC;

SELECT
peer_group,
COUNT(*) AS companies
FROM peer_groups
GROUP BY peer_group;

SELECT COUNT(*) AS total_stock_records
FROM stock_prices;