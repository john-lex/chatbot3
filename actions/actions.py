# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
from flask import Flask, jsonify
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

order_pizza = []


class ActionPlaceOrder(Action):
  def name(self):
    return "place_order_pizza"
  
  def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
    name = tracker.get_slot("name")
    type_pizza = tracker.get_slot("type_pizza")
    size_pizza = tracker.get_slot("size_pizza")
    address = tracker.get_slot("address")
    phone = tracker.get_slot("phone")
    costo_pizza = tracker.get_slot("costo_pizza")

    precio_ = precio_pizza(size_pizza)

    order = {
      "name" : name,
      "phone" : phone,
      "address" : address,
      "type_pizza" : type_pizza,
      "siza_pizza" : size_pizza
    }

    order_pizza.append(order)

    message_confirmation = (
            f"Tu orden ha sido registrada exitosamente, señor(a) {name}. "
            f"Su pedido: Pizza {type_pizza} de tamaño {size_pizza}. "
            f"Dirección de envío: {address}. "
            f"Teléfono: {phone}. "
            f"Tiene un costo de ${precio_}. "
            f"Su orden llegará de 20 a 30 minutos, gracias por preferirnos."
        )
    
    dispatcher.utter_message(text=message_confirmation)

    return []
  

def precio_pizza(size_pizza):
   
  precios = {
          "pequeña": 5,
          "mediana": 10,
          "grande": 15,
  }

  precio = precios.get(size_pizza.lower(), "desconocido")

  if size_pizza == "desconocido":
     return f"Lo siento, no tenemos información sobre el tamaño de pizza '{size_pizza}'."
  else:
     return precio
  

class ActionPrecioPizza(Action):

    def name(self) -> Text:
        return "action_obtener_precio_pizza"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        tamaño = tracker.get_slot("size_pizza")

        precios = {
            "pequeña": 5,
            "mediana": 10,
            "grande": 15,
            
        }

        precio = precios.get(tamaño.lower(), "desconocido")

        if precio == "desconocido":
            dispatcher.utter_message(text=f"Lo siento, no tenemos información sobre el tamaño de pizza '{tamaño}'.")
        else:
            dispatcher.utter_message(text=f"El precio de una pizza {tamaño} es {precio} dólares.")

        return [SlotSet("costo_pizza", precio)]