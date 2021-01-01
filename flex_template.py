from stock_function import name, capacity, accu_capacity, accu_capacity_multi, estimated_capacity
def flex_template(stock_name, stock_capacity, stock_esti_capacity):
    flex_box =  {
                "type" : "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": stock_name,
                            "weight": "bold",
                            "size": "xl"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "margin": "lg",
                            "spacing": "sm",
                            "contents": [
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": "昨日成交量",
                                    "color": "#aaaaaa",
                                    "size": "sm",
                                    "flex": 1
                                },
                                {
                                    "type": "text",
                                    "text": stock_capacity,
                                    "wrap": True,
                                    "color": "#666665",
                                    "size": "sm",
                                    "flex": 2
                                }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": "今日預估量",
                                    "color": "#aaaaaa",
                                    "size": "sm",
                                    "flex": 1
                                },
                                {
                                    "type": "text",
                                    "text": stock_esti_capacity,
                                    "wrap": True,
                                    "color": "#666665",
                                    "size": "sm",
                                    "flex": 2
                                }
                                ]
                            }
                            ]
                        }
                    ]
                }
            }

    return flex_box

# return multiple estimated capacity in one flex box
def flex_template_multi(stock_nums):
    flex_box =  {
                "type" : "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": '預估量',
                            "weight": "bold",
                            "size": "xl"
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "margin": "lg",
                            "spacing": "sm",
                            "contents": [
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": "股票名稱",
                                    "color": "#aaaaaa",
                                    "size": "sm",
                                    "flex": 1
                                }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": "昨日成交量",
                                    "color": "#aaaaaa",
                                    "size": "sm",
                                    "flex": 1
                                }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": "今日預估量",
                                    "color": "#aaaaaa",
                                    "size": "sm",
                                    "flex": 1
                                }
                                ]
                            }
                            ]
                        }
                    ]
                }
            }
    
    flex_box['body']['contents'] = flex_box['body']['contents'] + flex_content(stock_nums)

    return flex_box

def flex_content(stock_dict):
    stock_column = []
    stock_nums = [stock_num for stock_num, stock_capacity in stock_dict.items()]
    stock_accu_capacitys = accu_capacity_multi(stock_nums)
    stock_accu_capacitys_dict = {stock_nums[i]:stock_accu_capacitys[i] for i in range(len(stock_nums))}
    for stock_num, stock_capacity in stock_dict.items():
        stock_raw = {
                "type": "box",
                "layout": "horizontal",
                "margin": "lg",
                "spacing": "sm",
                "contents": []
            }
        stock_name = name(stock_num)
        stock_accu_capacity = str(stock_accu_capacitys_dict[stock_num])
        stock_esti_capacity = str(estimated_capacity(stock_accu_capacity))

        stock_raw['contents'].append(single_block(stock_name))
        stock_raw['contents'].append(single_block(str(stock_capacity)))
        stock_raw['contents'].append(single_block(stock_esti_capacity))

        stock_column.append(stock_raw)

    return stock_column

def single_block(text):
    stock_block = {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
            {
                "type": "text",
                "text": text,
                "color": "#aaaaaa",
                "size": "sm",
                "flex": 1
            }
            ]
        }

    return stock_block
