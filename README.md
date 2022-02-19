# HACKATON
A task: 
Analyze and recreate the application from the provided data. The application should have sections:

1. Analytics (in various slices of data)
2. List of all orders with the ability to search by status, etc.
3. Complete life cycle of an order (order placement, proposal submission, order execution, etc.)
Description of events:
1. OrderEvent - a delivery order from a client.
2. OfferEvent - an offer from a logistics company.
3. OfferAcceptEvent - the client has accepted the offer.
4. OrderCancelEvent - order cancellation
5. OrderFreightReceiveEvent - an order has been received for shipment from a warehouse/shop by a logistics company.
6. OrderFulfillmentEvent - the order has been completed.
7. OrderFailEvent - order failed.
