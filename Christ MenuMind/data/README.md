Christ MenuMind – Synthetic CSV Dataset

IMPORTANT: All menu prices, menus, sales, ratings, reviews, student preferences, footfall and operational metrics are synthetic/demo data. Outlet names and block mapping follow the list supplied for this project, but menu items and performance figures have not been independently verified with the real outlets. Never present simulated sales as actual campus sales.

FILES
- blocks.csv: 5 blocks and outlet counts.
- outlets.csv: 28 outlets with block mapping and illustrative outlet metadata.
- menu_items.csv: 980 menu items (35 per outlet: 28 vegetarian + 7 chicken-only), prices, categories, ratings, prep time, calories, tags, allergens and estimated item cost.
- sales_data.csv: 60 days of simulated daily item-level quantity, gross/net sales, discounts and estimated profit.
- student_reviews.csv: 3,200 synthetic reviews with rating dimensions and short review text.
- student_preferences.csv: 800 synthetic student preference profiles for recommender testing.
- price_history.csv: 3 illustrative price snapshots per menu item.
- outlet_daily_operations.csv: 60 days of simulated footfall, orders, wait time, satisfaction, stockouts and food waste.

RELATIONSHIPS
blocks.block_id -> outlets.block_id
outlets.outlet_id -> menu_items.outlet_id
menu_items.item_id -> sales_data.item_id
menu_items.item_id -> student_reviews.item_id
menu_items.item_id -> price_history.item_id
outlets.outlet_id -> outlet_daily_operations.outlet_id

DASHBOARD IDEAS
1. Campus overview: outlet count, menu count, revenue, quantity sold, sales trend and top categories.
2. Block analytics: filter by block and compare outlets.
3. Outlet analytics: menu mix, price distribution, top items, daily sales and operations.
4. Menu intelligence: vegetarian/chicken split, category mix, ratings, prep time and calories.
5. Meal recommender: budget + food type + category + block + availability; rank results using rating and simulated sales popularity.
6. Student feedback: rating distribution, value-for-money, taste and portion scores.
7. Operations: estimated footfall, order volume, wait time, stockouts and food waste.

RECOMMENDER
Filter menu_items.csv by price_inr, food_type, category, block_name and availability_status. Rank results using average_rating and quantity_sold aggregated from sales_data.csv. Student preferences are synthetic profiles for demonstration only.

FOOD RULES
- Non-vegetarian entries are chicken-only; no fish, seafood, mutton, beef or pork.
- Vegetarian entries are labelled vegetarian, but confirm recipes and egg-free status with outlets before presenting dietary guarantees.
- Chicken Caesar salad is explicitly bacon-free.

DATA COVERAGE
60 days ending 17 November 2026. All records are synthetic/demo data.
