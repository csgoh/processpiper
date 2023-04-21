from processpiper.text2diagram import render

input_syntax = """
title: Sample Test Process
colourtheme: GREENTURTLE
lane: End User
    (start) as start
    [Enter Keyword] as enter_keyword
    (end) as end
    
start->enter_keyword->end
"""

input_syntax = """
title: Pizza Order Process
            colourtheme: BLUEMOUNTAIN
            lane: Customer
                    (start) as start
                    [Browse PizzaPiper website] as browse_website
                    [Order a pizza] as order_pizza
                    [Make payment] as make_payment
                    [Receive pizza] as receive_pizza
                    (end) as end
            pool: Pizza Piper Enterprise
                lane: Pizza Shop
                    [Receive order] as receive_order
                    [Bake pizza] as bake_pizza
                    <Pizza ready?> as pizza_ready
                lane: Pizza Delivery
                    [Deliver pizza] as deliver_pizza


        start->browse_website->order_pizza->make_payment
        make_payment-"Order details"->receive_order->bake_pizza
        bake_pizza->pizza_ready
        pizza_ready-"Yes"->deliver_pizza-"Freshly baked \\npizza"->receive_pizza
        pizza_ready-"No"->bake_pizza
        receive_pizza->end


            footer: Generated by Process Piper
            """

render(input_syntax, "pizza-order-process.png")
