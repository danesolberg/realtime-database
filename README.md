# realtime-database
Prototype server for realtime push updates via websockets to clients issuing SQL queries

https://user-images.githubusercontent.com/25882507/175367472-7a76244f-cc4f-409a-8a42-d707b1c9c3bd.mov

## Subscription Algorithm
- Analyzes the predicate conditions of SQL query WHERE clauses (e.g. AND/OR statement consisting of numerous boolean conditions (GT, LT, EQ, etc.)) and inserts each condition into a n-ary subscription tree data structure.
- Calculates the effective key ranges for each boolean condition (e.g. age<51 equates to a key range of (-inf, 50]) and inserts them into a recursive RangeMap data structure.
- Tracks when a predicate clause is completed and tracks subscribed queries at the appropriate level of the subscription tree.
- Database [Change Data Capture](https://en.wikipedia.org/wiki/Change_data_capture) data mutation streams are checked against this subscription tree by using a standard Depth First Search for matching RangeMap entries with subscribed queries.

![Screen Shot 2022-06-22 at 14 21 10](https://user-images.githubusercontent.com/25882507/175369206-d61d6526-fa87-443d-ba3d-bb7d95428058.png)


## TODO
- Tests
### Query feature support
- Add support for joins and aggregate/window functions in SQL queries
- Add in-memory processing layer to recompute results and send partial results for aggregate functions (count, max, limit, etc)
### Client library
- Build out client API beyond current React/websocket prototype
### Architecture
- Loosen coupling between functional components. Allow client to write queries in multiple languages (even raw SQL ideally), and create mapper objects to convert between query syntax and backend nested predicate objects.  Allow for alternative db management frameworks beyond SQLAlchemy (support true CDC when available)
- Define clearer responsibility boundaries and connection interface contracts/guarantees to improve extensibility
