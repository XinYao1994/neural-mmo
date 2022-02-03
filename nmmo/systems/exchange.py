from pdb import set_trace as T

from collections import defaultdict, deque
from queue import PriorityQueue
import inspect

import math

class Offer:
   def __init__(self, seller, item):
      self.seller = seller
      self.item   = item

   '''
   def __lt__(self, offer):
      return self.price < offer.price
      
   def __le__(self, offer):
      return self.price <= offer.price

   def __eq__(self, offer):
      return self.price == offer.price

   def __ne__(self, offer):
      return self.price != offer.price

   def __gt__(self, offer):
      return self.price > offer.price

   def __ge__(self, offer):
      return self.price >= offer.price
   '''

#Why is the api so weird...
class Queue(deque):
   def __init__(self):
      super().__init__()
      self.price = None

   def push(self, x):
      self.appendleft(x)
   
   def peek(self):
      if len(self) > 0:
         return self[-1]
      return None

class ItemListings:
   def __init__(self):
      self.listings    = PriorityQueue()
      self.placeholder = None
      self.item_number = 0
      self.alpha       = 0.01

      self.step()

   def step(self):
      self.volume = 0

   @property
   def price(self):
      if not self.supply:
          return

      price, item_number, seller = self.listings.get()
      self.listings.put((price, item_number, seller))
      return price

   @property
   def supply(self):
      return self.listings.qsize()

   @property
   def empty(self):
      return self.listings.empty()

   def buy(self, buyer, quantity, max_price):
      if not self.supply:
         return

      price, item_number, seller = self.listings.get()

      if price > max_price or price > buyer.inventory.gold.quantity.val:
         self.listings.put((price, item_number, seller))
         return

      seller.inventory.gold.quantity += price
      buyer.inventory.gold.quantity  -= price

      buyer.buys   += 1
      seller.sells += 1
      self.volume  += 1
      return price
         
   def sell(self, seller, quantity, price):
      if price == 1 and not self.empty:
         seller.inventory.gold.quantity += 1
      else:
         self.listings.put((price, self.item_number, seller))
         self.item_number += 1

      #print('Sell {}: {}'.format(item.__class__.__name__, price))

class Exchange:
   def __init__(self):
      self.item_listings = defaultdict(ItemListings)

   @property
   def dataframeKeys(self):
      keys = []
      for listings in self.item_listings.values():
         if listings.placeholder:
            keys.append(listings.placeholder.instanceID)
      return keys

   def step(self):
      for item, listings in self.item_listings.items():
         listings.step()

   def available(self, item):
      return self.item_listings[item].available()

   def buy(self, realm, buyer, item, quantity):
      if __debug__:
         assert isinstance(item, object)

      #TODO: Handle ammo stacks
      if not buyer.inventory.space:
         return

      level        = item.level.val

      #Agents may try to buy an item at the same time
      #Therefore the price has to be semi-variable
      price        = item.price.val
      max_price    = 1.1 * price

      item         = type(item)
      listings_key = (item, level)
      listings     = self.item_listings[listings_key]

      price = listings.buy(buyer, quantity, max_price)
      if price:
         #print('{} Bought {} for {}.'.format(buyer.base.name, item.__name__, price))
         buyer.inventory.receive(listings.placeholder)

         #Update placeholder
         listings.placeholder = None
         if listings.supply:
            listings.placeholder = item(realm, level, price=listings.price)
            
   def sell(self, realm, seller, item, quantity, price):
      if __debug__:
         assert isinstance(item, object)
         assert item in seller.inventory
         assert item.quantity.val > 0

      quantity = item.quantity.val
      level    = item.level.val

      #Unequip from seller
      seller.inventory.remove(item)
      item = type(item)

      listings_key  = (item, level)
      listings      = self.item_listings[listings_key]
      current_price = listings.price

      #Update obs placeholder item
      if listings.placeholder is None or (current_price is not None and price < current_price):
         listings.placeholder = item(realm, level, price=price, quantity=quantity)

      #print('{} Sold {} x {} for {} ea.'.format(seller.base.name, quantity, item.__name__, price))
      listings.sell(seller, quantity, price)
